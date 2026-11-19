#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
发布器：把 _staging/<week>/ 里复审通过的候选移入 articles/，
自动挂到 README 对应板块 + 写本周更新日志 + 重建 articles/INDEX.md。

用法:
  python tools/publish.py --week 2026-W46 --pick 01,03,05
  python tools/publish.py --week 2026-W46 --pick 01 --no-commit
  python tools/publish.py --list --week 2026-W46
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
ARTICLES = os.path.join(ROOT, "articles")
STAGING = os.path.join(ROOT, "_staging")
STATE = os.path.join(ROOT, "data", "state.json")
BUDGET_MB = 60

CST = timezone(timedelta(hours=8))

# README 中真实存在的板块（二级标题），顺序同时决定索引的分组
DEVICE_ORDER = [
    "Openwrt", "摄像头", "无人机", "车机", "充电桩", "基站", "防火墙", "卫星安全",
    "打印机", "智能家居", "机器人", "芯片安全", "RFID", "WIFI安全", "协议安全",
    "硬件钱包", "FUZZ",
]
TECH_ORDER = ["安全启动", "固件解密", "故障注入", "绕过ASLR"]
RES_ORDER = ["固件下载", "虚拟机镜像", "杂项"]
SECTIONS = DEVICE_ORDER + TECH_ORDER + RES_ORDER


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def parse_front_matter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    block = text[3:end]
    meta = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v.startswith('"') and v.endswith('"'):
            try:
                v = json.loads(v)
            except Exception:
                v = v.strip('"')
        meta[k] = v
    body = text[end + 4:]
    return meta, body


def section_anchor(name):
    return name


HEADING_RE = re.compile(r"^#{1,2} ")


def insert_link_into_section(readme_text, section, line):
    lines = readme_text.split("\n")
    head_idx = None
    for i, ln in enumerate(lines):
        if ln.strip() in ("# " + section, "## " + section):
            head_idx = i
            break
    if head_idx is None:
        return None
    end_idx = len(lines)
    for j in range(head_idx + 1, len(lines)):
        if HEADING_RE.match(lines[j]):
            end_idx = j
            break
    last_item = None
    empty_note = None
    for j in range(head_idx + 1, end_idx):
        if lines[j].startswith("- "):
            last_item = j
        if empty_note is None and lines[j].strip().startswith("暂无"):
            empty_note = j
    if last_item is not None:
        lines.insert(last_item + 1, line)
    elif empty_note is not None:
        lines[empty_note] = line
    elif head_idx + 1 < end_idx and lines[head_idx + 1].strip() == "":
        lines.insert(head_idx + 2, line)
    else:
        lines.insert(head_idx + 1, "")
        lines.insert(head_idx + 2, line)
    return "\n".join(lines)


def append_log_entry(readme_text, date_str, week, body_lines):
    lines = readme_text.split("\n")
    head_idx = None
    for i, ln in enumerate(lines):
        if ln.strip() in ("# Log", "## Log", "## 更新日志", "# 更新日志"):
            head_idx = i
            break
    if head_idx is None:
        return None
    end_idx = len(lines)
    for j in range(head_idx + 1, len(lines)):
        if HEADING_RE.match(lines[j]):
            end_idx = j
            break
    summary_idx = None
    for j in range(head_idx + 1, end_idx):
        if "<summary>" in lines[j]:
            summary_idx = j
            break
    heading = "### " + date_str + ((" · " + week) if week else "")
    block = [heading, ""] + list(body_lines) + [""]
    if summary_idx is not None:
        insert_at = summary_idx + 1
        if insert_at < end_idx and lines[insert_at].strip() == "":
            insert_at += 1
        lines[insert_at:insert_at] = block
        return "\n".join(lines)
    close_indices = [j for j in range(head_idx + 1, end_idx) if lines[j].strip() == "</details>"]
    if not close_indices:
        return None
    insert_at = close_indices[-1]
    lines[insert_at:insert_at] = (["", "<details>", "<summary>" + date_str + "</summary>", "", ">更新"]
                                  + list(body_lines) + ["", "", "</details>"])
    return "\n".join(lines)


def github_date(dt):
    return "%d/%d/%d" % (dt.month, dt.day, dt.year)


def rebuild_index():
    rows = []
    for dirpath, dirnames, filenames in os.walk(ARTICLES):
        for fn in sorted(filenames):
            if not fn.endswith(".md") or fn == "INDEX.md":
                continue
            path = os.path.join(dirpath, fn)
            meta, _ = parse_front_matter(read(path))
            if meta.get("status") != "published":
                continue
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            rows.append((meta.get("published", "")[:10] or meta.get("published_at", "")[:10],
                         meta.get("category", "杂项"), meta.get("title", fn), rel,
                         meta.get("source", ""), meta.get("score", ""), meta.get("url", "")))
    rows.sort(reverse=True)
    out = ["# 文章快照索引", "",
           "共 " + str(len(rows)) + " 篇已归档（每周自动抓取 + 复审）。快照仅供安全研究参考，版权归原作者所有。",
           "", "| 日期 | 板块 | 标题 | 快照 | 来源 |", "|:--|:--|:--|:--|:--|"]
    for date, cat, title, rel, source, score, url in rows:
        out.append("| %s | %s | [%s](%s) | [md](%s) | %s |"
                   % (date, cat, title.replace("|", "/"), url, rel, source))
    write(os.path.join(ARTICLES, "INDEX.md"), "\n".join(out) + "\n")
    return len(rows)


def _section_counts(readme_text):
    counts = {}
    current = None
    for ln in readme_text.split("\n"):
        s = ln.strip()
        if s.startswith("## "):
            current = s[3:].strip()
            counts.setdefault(current, 0)
            continue
        if s.startswith("# "):
            current = None
            continue
        if current and s.startswith("- "):
            counts[current] = counts.get(current, 0) + 1
    return counts


def _index_table(group, counts, pairs_per_row=3):
    out = ["| 板块 | 篇 " * pairs_per_row + "|", "|:--|--:" * pairs_per_row + "|"]
    for i in range(0, len(group), pairs_per_row):
        cells = []
        for k in range(pairs_per_row):
            if i + k < len(group):
                sec = group[i + k]
                cells.append("| [%s](#%s) | %d " % (sec, sec.lower(), counts.get(sec, 0)))
            else:
                cells.append("| | ")
        out.append("".join(cells) + "|")
    return out


def rebuild_index_block():
    """按各板块实际条目数重写 <!-- INDEX:START --> … <!-- INDEX:END --> 区块。"""
    text = read(README)
    start = text.find("<!-- INDEX:START -->")
    end = text.find("<!-- INDEX:END -->")
    if start < 0 or end < 0 or end < start:
        return 0
    counts = _section_counts(text)
    rows = 0
    for dirpath, _, filenames in os.walk(ARTICLES):
        rows += len([f for f in filenames if f.endswith(".md") and f != "INDEX.md"])
    block = ["<!-- INDEX:START -->", "", "**设备与场景**", ""]
    block += _index_table(DEVICE_ORDER, counts, 3)
    block += ["", "**技术专题**", ""]
    block += _index_table(TECH_ORDER, counts, 2)
    block += ["", "**资源与归档**", ""]
    block += _index_table(RES_ORDER, counts, 3)
    block += ["| [文章快照](articles/INDEX.md) | %d | [更新日志](#更新日志) | - "
              "| [收录标准](#收录标准) | - |" % rows, "", "<!-- INDEX:END -->"]
    rest = text[end + len("<!-- INDEX:END -->"):]
    write(README, text[:start] + "\n".join(block) + rest)
    return rows


def rebuild_latest_block(limit=8):
    """重写 README 里 <!-- LATEST:START --> … <!-- LATEST:END --> 之间的「最新归档」表格。"""
    rows = []
    for dirpath, dirnames, filenames in os.walk(ARTICLES):
        for fn in sorted(filenames):
            if not fn.endswith(".md") or fn == "INDEX.md":
                continue
            path = os.path.join(dirpath, fn)
            meta, _ = parse_front_matter(read(path))
            if meta.get("status") != "published":
                continue
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            rows.append((meta.get("published", "")[:10], meta.get("category", "杂项"),
                         meta.get("title", fn), rel))
    if not rows:
        return 0
    rows.sort(reverse=True)
    out = ["| 日期 | 板块 | 文章 |", "|:--|:--|:--|"]
    for date, cat, title, rel in rows[:limit]:
        out.append("| %s | %s | [%s](%s) |" % (date, cat, title.replace("|", "/"), rel))
    text = read(README)
    start = text.find("<!-- LATEST:START -->")
    end = text.find("<!-- LATEST:END -->")
    if start < 0 or end < 0 or end < start:
        return 0
    new_text = (text[:start] + "<!-- LATEST:START -->\n" + "\n".join(out) + "\n"
                + text[end:])
    write(README, new_text)
    return len(rows)


def repo_size():
    total = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in dirpath.split(os.sep) or "_staging" in dirpath.split(os.sep):
            continue
        for fn in filenames:
            try:
                total += os.path.getsize(os.path.join(dirpath, fn))
            except OSError:
                pass
    return total


def git(args):
    p = subprocess.run(["git"] + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", default="")
    ap.add_argument("--pick", default="", help="comma separated staging numbers, e.g. 01,03")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--no-commit", action="store_true")
    args = ap.parse_args()

    weeks = sorted(os.listdir(STAGING)) if os.path.isdir(STAGING) else []
    week = args.week or (weeks[-1] if weeks else "")
    if not week:
        print("no staging dir; run tools/crawl.py first")
        return 1
    sdir = os.path.join(STAGING, week)
    man_path = os.path.join(sdir, "manifest.json")
    manifest = json.loads(read(man_path)) if os.path.exists(man_path) else {"items": []}
    # 以目录里的快照文件为准（manifest 可能被后续抓取覆盖）
    staged = []
    for fn in sorted(os.listdir(sdir)):
        if not fn.endswith(".md") or not fn[:2].isdigit():
            continue
        meta, _ = parse_front_matter(read(os.path.join(sdir, fn)))
        if meta.get("status") != "candidate":
            continue
        try:
            score = float(meta.get("score") or 0)
        except ValueError:
            score = 0.0
        staged.append({"file": fn, "score": score, "category": meta.get("category", "杂项"),
                       "title": meta.get("title", fn), "url": meta.get("url", ""),
                       "source": meta.get("source", ""), "published": meta.get("published", "")})

    if args.list or not args.pick:
        print("staged candidates in " + week + ":")
        for it in staged:
            print("  %s  %5.1f  %-10s %s" % (it["file"][:2], it["score"], it["category"], it["title"][:80]))
        if not args.pick:
            print("\nuse --pick 01,03 to publish")
            return 0

    picks = set(x.strip() for x in args.pick.split(",") if x.strip())
    chosen = [i for i in staged if i["file"][:2] in picks]
    if not chosen:
        print("nothing matched --pick " + args.pick)
        return 1

    readme = read(README)
    now = datetime.now(CST)
    today = now.strftime("%Y-%m-%d")
    published = []

    for rec in chosen:
        src_path = os.path.join(sdir, rec["file"])
        if not os.path.exists(src_path):
            print("missing file: " + src_path)
            continue
        text = read(src_path)
        meta, body = parse_front_matter(text)
        cat = rec.get("category") or meta.get("category") or "杂项"
        if cat not in SECTIONS:
            cat = "杂项"
        day = (meta.get("published") or today)[:10]
        fname = day + "-" + rec["file"][3:]
        dest_dir = os.path.join(ARTICLES, cat)
        dest = os.path.join(dest_dir, fname)
        new_meta = list(meta.items())
        meta_txt = ["---"]
        for k, v in meta.items():
            if k == "status":
                meta_txt.append("status: published")
            elif k == "published_at":
                continue
            elif k == "category":
                meta_txt.append("category: " + json.dumps(cat, ensure_ascii=False))
            elif k in ("title", "source"):
                meta_txt.append(k + ": " + json.dumps(v, ensure_ascii=False))
            else:
                meta_txt.append(k + ": " + str(v))
        meta_txt.append("published_at: " + now.isoformat())
        meta_txt.append("---")
        write(dest, "\n".join(meta_txt) + "\n\n" + body.lstrip("\n"))

        rel = os.path.relpath(dest, ROOT).replace(os.sep, "/")
        title = rec["title"]
        link = "- [" + title + "](" + rel + ") · [原文](" + rec["url"] + ")"
        new_readme = insert_link_into_section(readme, cat, link)
        if new_readme is None:
            new_readme = insert_link_into_section(readme, "杂项", link)
        if new_readme:
            readme = new_readme
        published.append((rec, cat, rel, link))
        print("published: " + rel)

    if published:
        log_lines = []
        for rec, cat, rel, link in published:
            log_lines.append("- [" + rec["title"] + "](" + rel + ") —— " + cat)
        new_readme = append_log_entry(readme, today, week, log_lines)
        write(README, new_readme if new_readme else readme)

        # 已发布的条目从 staging 删除，避免下次重复
        for rec, cat, rel, link in published:
            p = os.path.join(sdir, rec["file"])
            if os.path.exists(p):
                os.remove(p)

        n = rebuild_index()
        rebuild_latest_block()
        rebuild_index_block()
        size_mb = repo_size() / 1048576.0
        print("articles index rebuilt: %d published, repo size %.1f MB / budget %d MB" % (n, size_mb, BUDGET_MB))
        if size_mb > BUDGET_MB:
            print("WARNING: repo over budget, consider pruning old snapshots")

        if not args.no_commit:
            code, out, err = git(["add", "-A"])
            msg = "每周更新 " + week + "：新增 " + str(len(published)) + " 篇"
            code, out, err = git(["commit", "-m", msg])
            print(out or err)
    return 0


if __name__ == "__main__":
    sys.exit(main())
