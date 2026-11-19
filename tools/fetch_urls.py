#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
按 URL 清单直接归档（用于补齐特定方向的公开资料）。

用法:
  python tools/fetch_urls.py --spec ..\_targets.json --week 2026-W49

spec 每项:
  {"url": "...", "title": "...", "source": "...", "published": "YYYY-MM-DD",
   "category": "故障注入", "mode": "page" | "meta", "summary": "...", "notes": "## 收录理由\n\n- ..."}
mode=page: 抓正文（遵守 robots、慢速串行）
mode=meta: 不抓正文（PDF/论文/需要登录的页面），只存元数据 + 摘要
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import crawl

CST = timezone(timedelta(hours=8))
ROOT = crawl.ROOT


def slug(title, maxlen=60):
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", title, flags=re.UNICODE).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return (s or "article")[:maxlen].strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--week", required=True)
    args = ap.parse_args()

    conf = crawl.load_json(crawl.CONF_PATH, {})
    pol = crawl.Politeness(conf.get("politeness", {}))
    max_bytes = int(conf.get("politeness", {}).get("max_article_bytes", 150000))

    spec = json.load(open(args.spec, "r", encoding="utf-8"))
    outdir = os.path.join(crawl.STAGING_ROOT, args.week)
    os.makedirs(outdir, exist_ok=True)
    now = datetime.now(CST)

    n = 0
    for item in spec:
        n += 1
        num = "%02d" % n
        url = item["url"]
        title = item["title"]
        body_mode = "meta"
        text = ""
        if item.get("mode", "meta") == "page":
            try:
                raw, ctype, final = pol.fetch(url, max_bytes + 400000)
                text = crawl.extract_main_text(raw.decode("utf-8", "replace"), final)
                if len(text) < 800:
                    text = crawl.extract_from_embedded_json(raw.decode("utf-8", "replace"))
                if len(text) >= 400:
                    body_mode = "fulltext"
                else:
                    text = ""
                    print("  [meta-fallback] %s" % url)
            except Exception as e:
                print("  [fetch-fail] %s (%s)" % (url, type(e).__name__))
        if body_mode == "meta":
            text = (item.get("summary") or "").strip()
        if len(text.encode("utf-8")) > max_bytes:
            text = text.encode("utf-8")[:max_bytes].decode("utf-8", "ignore") + "\n\n_[truncated]_"
        sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        fm = [
            "---",
            "title: " + json.dumps(title, ensure_ascii=False),
            "source: " + json.dumps(item.get("source", ""), ensure_ascii=False),
            "url: " + url,
            "published: " + item.get("published", ""),
            "fetched: " + now.isoformat(),
            "category: " + json.dumps(item.get("category", "杂项"), ensure_ascii=False),
            "score: 0",
            "keywords: " + json.dumps(item.get("keywords", []), ensure_ascii=False),
            "sha256: " + sha,
            "bytes: " + str(len(text.encode("utf-8"))),
            "truncated: false",
            "body_mode: " + body_mode,
            "status: candidate",
            "---",
            "",
            "# " + title,
            "",
            "> 来源：" + item.get("source", "") + " · " + item.get("published", "") + " · [原文](" + url + ")",
            "> 归档用于安全研究参考；版权归原作者所有。",
            "",
        ]
        if body_mode == "meta":
            fm.extend(["> ⚠️ 本条为「元数据 + 摘要」归档（论文/PDF/前端渲染页面），完整内容请读原文。", ""])
        if item.get("notes"):
            fm.append(item["notes"].strip())
            fm.append("")
        fname = "%s-%s.md" % (num, slug(title))
        with open(os.path.join(outdir, fname), "w", encoding="utf-8") as f:
            f.write("\n".join(fm) + "\n" + text + "\n")
        print("%s %-10s %-8s %s" % (num, body_mode, item.get("category"), title[:70]))
    print("done:", n, "->", os.path.relpath(outdir, ROOT), "| requests:", pol.requests_made)


if __name__ == "__main__":
    sys.exit(main())
