#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
IOTsec-all-in-one 周更爬虫 (weekly crawl)

设计原则（请勿修改成"更快/更猛"的版本）：
  1. 只读公开 RSS/Atom，然后像普通浏览器一样逐篇访问文章页；
  2. 全程串行，默认每次请求间隔 8s + 随机抖动，遵守 robots.txt 与 Crawl-delay；
     绝不登录、不伪造 Cookie、不绕过任何访问控制、不碰登录墙/付费墙；
  3. 单篇截断 + 单次下载总量上限 + 仓库体积预算 + 磁盘剩余空间下限，
     避免把本地/仓库撑爆；
  4. 抓到的文章先落到 _staging/<week>/ 等待复审（脚本不做"发布"决定），
     只有复审认为"攻击角度新颖 或 利用难度极高"的条目才由 publish.py 移入 articles/。

用法:
  python tools/crawl.py                    # 默认回溯 21 天
  python tools/crawl.py --days 8           # 周更模式
  python tools/crawl.py --dry-run          # 只看 feed，不下载正文
  python tools/crawl.py --limit 12         # 限制本次下载文章数
"""

import argparse
import hashlib
import json
import os
import random
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import ssl
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import feedparser
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_PATH = os.path.join(ROOT, "tools", "sources.json")
STATE_PATH = os.path.join(ROOT, "data", "state.json")
LOG_PATH = os.path.join(ROOT, "data", "crawl.log")
ARTICLES_DIR = os.path.join(ROOT, "articles")
STAGING_ROOT = os.path.join(ROOT, "_staging")

FENCE = chr(96) * 3
TICK = chr(96)

CST = timezone(timedelta(hours=8))


def log(msg):
    line = "[%s] %s" % (datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line, flush=True)
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ---------------------------------------------------------------- 质量打分
# 领域词：出现说明大概率属于 IoT / 固件 / 硬件 / 底层安全
DOMAIN_TERMS = [
    "firmware", "router", "iot", "embedded", "u-boot", "uboot", "bootloader", "baseband",
    "modem", "5g", "lte", "sim card", "smart card", "nfc", "rfid", "bluetooth", "ble",
    "zigbee", "lora", "wi-fi", "wifi", "wpa", "camera", "ipcam", "dvr", "nvr", "nas",
    "printer", "mfp", "drone", "uav", "mavlink", "automotive", "can bus", "ecu", "telematics",
    "charging", "charger", "ocpp", "satellite", "starlink", "gnss", "spi", "i2c", "uart",
    "jtag", "swd", "nand", "emmc", "nor flash", "spi flash", "secure boot", "verified boot",
    "trustzone", "tee", "secure enclave", "secure element", "hsm", "hardware wallet", "ledger",
    "trezor", "rowhammer", "dram", "ddr", "efuse", "soc", "mcu", "rtos", "vxworks", "qnx",
    "openwrt", "luci", "busybox", "ubiquiti", "tp-link", "tplink", "netgear", "d-link",
    "dlink", "hikvision", "dahua", "xerox", "fortinet", "fortios", "ivanti", "palo alto",
    "sonicwall", "check point", "zyxel", "asus router", "synology", "qnap", "mikrotik",
    "industrial", "plc", "scada", "modbus", "opc ua", "mqtt", "coap", "canbus", "obd",
    "robot", "smart home", "home assistant", "zigbee2mqtt",
    "固件", "路由器", "摄像头", "无人机", "基站", "充电桩", "芯片", "硬件", "智能家居",
    "蓝牙", "协议", "刷机", "串口", "示波器", "逻辑分析仪", "电压毛刺", "故障注入",
    "侧信道", "功耗分析", "激光注入", "冷启动", "安全启动", "固件解密", "车机", "越权",
    # 安全设备 / 网络设备 / 固件生态
    "uefi", "bios", "tpm", "cpld", "fpga", "logic analyzer", "chipwhisperer", "emfi",
    "beyondtrust", "barracuda", "n-central", "citrix", "netscaler", "big-ip", "juniper",
    "pulse secure", "globalprotect", "pan-os", "ruckus", "aruba", "cambium", "switches",
    "access point", "nas", "sdn", "sd-wan", "cisco", "juniper", "arista", "f5",
    "ipmi", "bmc", "raid", "hypervisor", "esxi", "vpn appliance", "edge device",
    "hardware security module", "tpm2", "measured boot", "attestation", "jtagulator",
    "设备固件", "嵌入式", "物联网", "硬件安全", "刷入", "持久化",
    # 固件/芯片/启动链补充词
    "bios", "acpi", "smm", "smram", "thunderbolt", "pcie", "nvme", "bootrom", "boot rom",
    "mask rom", "otp", "qualcomm", "broadcom", "mediatek", "realtek", "esp32", "stm32",
    "nrf52", "optee", "kernel module", "device tree", "soldering", "oscilloscope",
    "power analysis", "glitching", "flash dump", "dump firmware", "firmware image",
    "固件分析", "固件逆向", "芯片解密", "烧录", "量产", "硬件调试", "拆解", "板载",
]

# 新颖性/难度词：出现说明"角度新"或"利用门槛高"
NOVELTY_TERMS = [
    "novel", "new class", "new technique", "new attack", "first-ever", "first public",
    "unprecedented", "previously unknown", "unexpected", "surprising", "overlooked",
    "forgotten", "rediscovered", "quirk", "design flaw", "protocol flaw", "fundamental flaw",
    "logic bug", "logic flaw", "unauthenticated", "pre-auth", "preauth", "zero-day",
    "0day", "0-day", "in the wild", "exploit chain", "pwn2own", "one-click", "wormable",
    "hard to exploit", "exploit primitive", "aslr bypass", "heap feng shui", "race condition",
    "physical access", "glitch", "fault injection", "side channel", "side-channel",
    "rowhammer", "sandbox escape", "kernel", "hypervisor", "bypass", "root cause",
    "from n-day", "full chain", "ssd", "microcode", "unpatchable", "permanent",
    "新型攻击", "新思路", "首次", "从未", "绕过", "逻辑漏洞", "设计缺陷", "未授权",
    "链式", "击穿", "突破", "关键漏洞", "硬核", "难度极高", "罕见", "深度剖析", "挖掘思路",
]

DEPTH_TERMS = [
    "cve", "exploit", "poc", "rce", "reverse engineering", "writeup", "deep dive",
    "analysis", "vulnerability", "privilege escalation", "arbitrary", "memory corruption",
    "漏洞", "复现", "逆向", "分析", "深度", "提权", "利用",
]

# 明显不属于本仓库主题（纯 IT/Web 应用层），用于扣分
OUT_OF_SCOPE_TERMS = [
    "wordpress", "joomla", "drupal", "thinkphp", "dedecms", "fastjson", "spring boot",
    "springboot", "struts", "weblogic", "jboss", "log4j", "shiro", "sql injection",
    "sql注入", "sql 注入", "xss", "csrf", "ssrf(web)", "cms", "graphql", "oauth",
    "chatgpt", "prompt injection", "llm jailbreak", "大模型", "gpt-4", "ai agent",
    "gartner", "compliance", "mdr", "soar", "scorecard", "trends", "webinar",
    "ctf", "大赛", "靶场", "writeup 比赛", "面试", "实习", "红队", "域渗透", "kerberos",
    "exchange server", "sharepoint", "active directory", "dify", "langchain",
]

NEGATIVE_TERMS = [
    "webinar", "webcast", "podcast", "hiring", "join our team", "we are excited to announce",
    "sponsor", "best practices", "how to protect", "how to secure", "checklist", "top 10",
    "roundup", "recap", "year in review", "survey", "product update", "release notes",
    "patch tuesday", "training", "course", "e-book", "awards", "conference recap",
    "如何防护", "最佳实践", "招聘", "培训", "直播", "课程", "活动预告", "年终总结",
    # 新闻/情报/软文类
    "threat intelligence report", "threat intelligence", "weekly roundup", "news roundup",
    "press release", "opinion", "interview", "announce", "news",
    "威胁情报", "周报", "月报", "简报", "快讯", "新闻",
]

# 分类推断：命中越多越优先（README 中的板块名）
CATEGORY_RULES = [
    ("摄像头", ["camera", "ipcam", "dvr", "nvr", "hikvision", "dahua", "tapo", "摄像头"]),
    ("无人机", ["drone", "uav", "mavlink", "dji", "无人机"]),
    ("车机", ["automotive", "can bus", "canbus", "obd", "ecu", "telematics", "tesla",
              "nissan", "car hacking", "车机", "车联网"]),
    ("充电桩", ["charging station", "charger", "evse", "ocpp", "充电桩"]),
    ("基站", ["baseband", "5g", "lte", "gnb", "enodeb", "srsran", "open5gs", "基站"]),
    ("卫星安全", ["satellite", "starlink", "gnss", "gps spoofing", "卫星"]),
    ("打印机", ["printer", "mfp", "xerox", "打印"]),
    ("Openwrt", ["openwrt", "luci", "router", "路由器", "busybox"]),
    ("智能家居", ["smart home", "mqtt", "home assistant", "zigbee", "matter", "智能家居", "智能音箱"]),
    ("RFID", ["rfid", "nfc", "mifare", "smart card", "校园卡"]),
    ("WIFI安全", ["wi-fi", "wifi", "wpa2", "wpa3", "802.11"]),
    ("协议安全", ["protocol", "bluetooth", "ble", "lora", "zigbee", "modbus", "协议"]),
    ("安全启动", ["secure boot", "verified boot", "bootloader", "u-boot", "uboot", "安全启动"]),
    ("固件解密", ["firmware encryption", "decrypt", "固件解密", "解包", "固件提取"]),
    ("故障注入", ["fault injection", "glitch", "voltage", "emfi", "laser", "故障注入", "毛刺"]),
    ("绕过ASLR", ["aslr", "rop", "信息泄露", "info leak"]),
    ("芯片安全", ["soc", "mcu", "silicon", "microcode", "rowhammer", "dram", "tee", "trustzone", "芯片"]),
    ("硬件钱包", ["hardware wallet", "ledger", "trezor", "硬件钱包"]),
    ("FUZZ", ["fuzzing", "afl", "libfuzzer", "honggfuzz", "fuzz"]),
    ("机器人", ["robot", "ros", "机器人"]),
    ("防火墙", ["fortinet", "fortios", "ivanti", "palo alto", "sonicwall", "check point", "防火墙", "vpn"]),
    ("杂项", []),
]


_RE_CACHE = {}


def _term_re(term):
    """ASCII 词用词边界匹配，避免 ecu->security / ble->vulnerable 这类误命中；中文用子串。"""
    pat = _RE_CACHE.get(term)
    if pat is None:
        if re.fullmatch(r"[a-z0-9 .+-]+", term):
            pat = re.compile(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])")
        else:
            pat = re.compile(re.escape(term))
        _RE_CACHE[term] = pat
    return pat


def count_hits(text, terms):
    low = text.lower()
    return [t for t in terms if _term_re(t).search(low)]


def score_entry(title, summary, trust=0.0):
    blob = (title + " " + summary).lower()
    d = count_hits(blob, DOMAIN_TERMS)
    n = count_hits(blob, NOVELTY_TERMS)
    p = count_hits(blob, DEPTH_TERMS)
    neg = count_hits(blob, NEGATIVE_TERMS) + count_hits(blob, OUT_OF_SCOPE_TERMS)
    score = (2.0 * min(len(d), 4) + 2.0 * min(len(n), 4) + 0.4 * min(len(p), 5)
             - 2.0 * min(len(neg), 4) + float(trust))
    return {"score": round(score, 2), "domain": d, "novelty": n, "depth": p,
            "negative": neg, "trust": float(trust)}


def is_relevant(signals):
    """必须有 IoT/固件/硬件/安全设备信号；或新颖性信号极强（新攻击面）；或来自一线研究团队。"""
    return (len(signals["domain"]) >= 1 or len(signals["novelty"]) >= 2
            or float(signals.get("trust", 0)) >= 2.0)


def infer_category(text, fallback):
    low = text.lower()
    best, best_hits = fallback, 0
    for name, terms in CATEGORY_RULES:
        hits = sum(1 for t in terms if _term_re(t).search(low))
        if hits > best_hits:
            best, best_hits = name, hits
    return best


# ---------------------------------------------------------------- feed 自动发现
def discover_feed_url(html, base):
    """页面不是 XML 时，从 <link rel="alternate" type="application/rss+xml"> 找真正的 feed 地址。"""
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        return ""
    for link in soup.find_all("link"):
        typ = (link.get("type") or "").lower()
        href = link.get("href") or ""
        if href and ("rss" in typ or "atom" in typ):
            return urllib.parse.urljoin(base, href)
    return ""


# ---------------------------------------------------------------- 礼貌抓取
class Politeness:
    def __init__(self, conf):
        self.min_interval = float(conf.get("request_min_interval_sec", 8))
        self.jitter = float(conf.get("request_jitter_sec", 4))
        self.timeout = float(conf.get("timeout_sec", 30))
        self.ua = conf.get("user_agent", "IOTsec-weekly-bot/1.0")
        self.respect_robots = bool(conf.get("respect_robots", True))
        self.max_requests = int(conf.get("max_requests_per_run", 40))
        self.requests_made = 0
        self.bytes_made = 0
        self._last = 0.0
        self._robots = {}
        proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or conf.get("proxy")
        handlers = [urllib.request.ProxyHandler({"http": proxy, "https": proxy})] if proxy else []
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        handlers.append(urllib.request.HTTPSHandler(context=ctx))
        self.opener = urllib.request.build_opener(*handlers)
        self.opener.addheaders = [("User-Agent", self.ua), ("Accept-Language", "en,zh;q=0.8")]

    def _sleep(self, host):
        delay = self.min_interval + random.uniform(0, self.jitter)
        robots = self._robots.get(host)
        if robots and robots.get("crawl_delay"):
            delay = max(delay, float(robots["crawl_delay"]))
        gap = time.time() - self._last
        if gap < delay:
            time.sleep(delay - gap)
        self._last = time.time()

    def _get_robots(self, url):
        parts = urllib.parse.urlsplit(url)
        host = parts.netloc
        if host in self._robots:
            return self._robots[host]
        entry = {"allow_all": True, "rules": [], "crawl_delay": None}
        robots_url = parts.scheme + "://" + host + "/robots.txt"
        try:
            self._sleep(host)
            req = urllib.request.Request(robots_url, headers={"User-Agent": self.ua})
            with self.opener.open(req, timeout=self.timeout) as r:
                raw = r.read(200000).decode("utf-8", "replace")
            for line in raw.splitlines():
                line = line.split("#")[0].strip()
                if not line or ":" not in line:
                    continue
                k, v = line.split(":", 1)
                k, v = k.strip().lower(), v.strip()
                if k == "disallow" and v:
                    entry["rules"].append(("disallow", v))
                elif k == "allow" and v:
                    entry["rules"].append(("allow", v))
                elif k == "crawl-delay":
                    try:
                        entry["crawl_delay"] = float(v)
                    except ValueError:
                        pass
        except Exception:
            entry["allow_all"] = True
        self._robots[host] = entry
        return entry

    def allowed(self, url):
        if not self.respect_robots:
            return True
        entry = self._get_robots(url)
        if entry["allow_all"] and not entry["rules"]:
            return True
        path = urllib.parse.urlsplit(url).path or "/"
        best_len, verdict = -1, True
        for kind, rule in entry["rules"]:
            if path.startswith(rule):
                if len(rule) > best_len:
                    best_len = len(rule)
                    verdict = (kind == "allow")
        return verdict

    def fetch(self, url, max_bytes):
        if self.requests_made >= self.max_requests:
            raise RuntimeError("max_requests_per_run reached")
        if not self.allowed(url):
            raise PermissionError("blocked by robots.txt: " + url)
        host = urllib.parse.urlsplit(url).netloc
        self._sleep(host)
        req = urllib.request.Request(url, headers={
            "User-Agent": self.ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })
        with self.opener.open(req, timeout=self.timeout) as r:
            ctype = r.headers.get("Content-Type", "")
            body = r.read(max_bytes)
            final = r.geturl()
        self.requests_made += 1
        self.bytes_made += len(body)
        return body, ctype, final


# ---------------------------------------------------------------- HTML -> Markdown
DROP_TAGS = {"script", "style", "noscript", "nav", "header", "footer", "aside", "form",
             "svg", "iframe", "button", "select", "input", "template"}
BLOCK_TAGS = {"p", "div", "section", "article", "main", "blockquote", "pre", "ul", "ol", "li",
              "h1", "h2", "h3", "h4", "h5", "h6", "table", "tr", "td", "th", "br", "hr",
              "dd", "dt"}


def abs_url(base, href):
    try:
        return urllib.parse.urljoin(base, href)
    except Exception:
        return href


def md_inline(node, base):
    if isinstance(node, NavigableString):
        return re.sub(r"\s+", " ", str(node))
    if not isinstance(node, Tag):
        return ""
    name = node.name.lower()
    if name in DROP_TAGS:
        return ""
    if name == "br":
        return "\n"
    if name == "hr":
        return "\n\n---\n\n"
    if name == "code":
        return TICK + node.get_text(" ", strip=True) + TICK
    if name == "a":
        text = node.get_text(" ", strip=True)
        href = abs_url(base, node.get("href", ""))
        if not text:
            return ""
        if not href or href.startswith("#"):
            return text
        return "[" + text + "](" + href + ")"
    if name == "img":
        alt = node.get("alt", "") or "image"
        src = abs_url(base, node.get("src", "") or node.get("data-src", ""))
        return "\n\n![" + alt + "](" + src + ")\n\n"
    if name == "pre":
        return "\n\n" + FENCE + "\n" + node.get_text("\n", strip=False).strip("\n") + "\n" + FENCE + "\n\n"
    return "".join(md_inline(c, base) for c in node.children)


def md_block(node, base):
    if isinstance(node, NavigableString):
        return re.sub(r"\s+", " ", str(node))
    if not isinstance(node, Tag):
        return ""
    name = node.name.lower()
    if name in DROP_TAGS:
        return ""
    if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        return "\n\n" + "#" * int(name[1]) + " " + node.get_text(" ", strip=True) + "\n\n"
    if name == "pre":
        return "\n\n" + FENCE + "\n" + node.get_text("\n", strip=False).strip("\n") + "\n" + FENCE + "\n\n"
    if name == "blockquote":
        inner = "".join(md_block(c, base) for c in node.children).strip()
        if not inner:
            return ""
        return "\n\n" + "\n".join("> " + ln.strip() for ln in inner.splitlines() if ln.strip()) + "\n\n"
    if name == "li":
        inner = "".join(md_block(c, base) for c in node.children).strip()
        return "\n- " + inner.replace("\n\n", "\n  ")
    if name in ("ul", "ol"):
        inner = "".join(md_block(c, base) for c in node.children)
        return "\n" + inner + "\n"
    if name == "tr":
        cells = [c.get_text(" ", strip=True) for c in node.children
                 if isinstance(c, Tag) and c.name in ("td", "th")]
        if not cells:
            return ""
        return "\n| " + " | ".join(cells) + " |"
    if name == "table":
        inner = "".join(md_block(c, base) for c in node.children)
        return "\n" + inner + "\n"
    if name in BLOCK_TAGS:
        inner = "".join(md_block(c, base) for c in node.children)
        if name in ("p", "div", "section", "article", "main", "dd", "dt"):
            return "\n\n" + inner.strip() + "\n\n"
        return "\n" + inner
    return "".join(md_inline(c, base) for c in node.children)


def _iter_long_strings(obj, depth=0):
    if depth > 14:
        return
    if isinstance(obj, str):
        if len(obj) > 500:
            yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            for s in _iter_long_strings(v, depth + 1):
                yield s
    elif isinstance(obj, list):
        for v in obj:
            for s in _iter_long_strings(v, depth + 1):
                yield s


def _clean_embedded_text(s):
    if "<" in s and ">" in s:
        s = BeautifulSoup(s, "lxml").get_text("\n", strip=True)
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def extract_from_embedded_json(html):
    """SPA 站点（正文在前端渲染）：从 JSON-LD articleBody 或 __NEXT_DATA__ 里抽正文。"""
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        return ""
    for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = tag.string or tag.get_text() or ""
        try:
            data = json.loads(raw)
        except Exception:
            continue
        for obj in (data if isinstance(data, list) else [data]):
            if isinstance(obj, dict):
                for key in ("articleBody", "text", "description"):
                    val = obj.get(key)
                    if isinstance(val, str) and len(val) > 800:
                        return _clean_embedded_text(val)
    best = ""
    for tag in soup.find_all("script"):
        raw = tag.string or tag.get_text() or ""
        if len(raw) < 2000:
            continue
        head = raw.lstrip()[:1]
        if head not in "{[":
            continue
        try:
            data = json.loads(raw)
        except Exception:
            continue
        for s in _iter_long_strings(data):
            if len(s) > len(best) and (" " in s or "\n" in s):
                best = s
    if len(best) > 800:
        return _clean_embedded_text(best)
    return ""


def extract_main_text(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    for t in soup(list(DROP_TAGS)):
        t.decompose()
    candidates = []
    for sel in ["article", "main", "[role=main]", "div.post-content", "div.entry-content",
                "div.article-content", "div.content", "div#content", "div.post", "body"]:
        for node in soup.select(sel):
            text = node.get_text(" ", strip=True)
            if len(text) > 600:
                candidates.append((len(text), node))
        if candidates:
            break
    if not candidates:
        return ""
    node = max(candidates, key=lambda x: x[0])[1]
    md = md_block(node, base_url)
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md


# ---------------------------------------------------------------- 工具函数
def slugify(title, maxlen=60):
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", title, flags=re.UNICODE).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    if not s:
        s = "article"
    return s[:maxlen].strip("-")


def entry_date(entry):
    for key in ("published_parsed", "updated_parsed"):
        val = entry.get(key)
        if val:
            try:
                return datetime(*val[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    for key in ("published", "updated"):
        val = entry.get(key)
        if val:
            try:
                dt = parsedate_to_datetime(val)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except Exception:
                pass
    return None


def strip_html(s, limit=1500):
    if not s:
        return ""
    txt = BeautifulSoup(s, "lxml").get_text(" ", strip=True)
    txt = re.sub(r"\s+", " ", txt)
    return txt[:limit]


def human_size(n):
    if n < 1024:
        return "%d B" % n
    if n < 1024 * 1024:
        return "%.1f KB" % (n / 1024.0)
    return "%.1f MB" % (n / 1048576.0)


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def week_key(dt):
    iso = dt.isocalendar()
    return "%04d-W%02d" % (iso[0], iso[1])


def repo_size_bytes(root):
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        parts = dirpath.split(os.sep)
        if ".git" in parts or "_staging" in parts:
            continue
        for fn in filenames:
            try:
                total += os.path.getsize(os.path.join(dirpath, fn))
            except OSError:
                pass
    return total


# ---------------------------------------------------------------- 主流程
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=21, help="lookback days")
    ap.add_argument("--limit", type=int, default=0, help="max articles to download (0=config)")
    ap.add_argument("--dry-run", action="store_true", help="score feeds only, no download")
    ap.add_argument("--min-score", type=float, default=3.0, help="min score to download")
    ap.add_argument("--reuse-manifest", default="", help="reuse candidates from an existing manifest.json (skips feed pass)")
    args = ap.parse_args()

    conf = load_json(CONF_PATH, {})
    polconf = conf.get("politeness", {})
    pol = Politeness(polconf)
    max_article_bytes = int(polconf.get("max_article_bytes", 150000))
    run_budget = int(polconf.get("max_download_bytes_per_run", 5000000))
    free_floor = float(polconf.get("disk_free_floor_gb", 2.0)) * (1024 ** 3)
    repo_budget = float(polconf.get("repo_size_budget_mb", 60)) * 1024 * 1024

    state = load_json(STATE_PATH, {"seen": {}, "runs": []})
    seen = state.get("seen", {})

    free = shutil.disk_usage(ROOT).free
    if free < free_floor:
        log("disk free %.1f GB below floor %.1f GB, abort" % (free / 1024.0 ** 3, free_floor / 1024.0 ** 3))
        return 2
    if repo_size_bytes(ROOT) > repo_budget:
        log("repo size over budget %.0f MB, prune first" % (repo_budget / 1048576.0))
        return 3

    now = datetime.now(CST)
    cutoff = now - timedelta(days=args.days)
    week = week_key(now)
    staging = os.path.join(STAGING_ROOT, week)
    os.makedirs(staging, exist_ok=True)

    max_fetch = args.limit or int(polconf.get("max_requests_per_run", 40))
    items = []

    log("crawl start: %d feeds, lookback %d days, min interval %.0fs"
        % (len(conf.get("feeds", [])), args.days, pol.min_interval))

    if args.reuse_manifest:
        prev = load_json(args.reuse_manifest, {})
        for it in prev.get("items", []):
            if it.get("status", "dry-run") in ("dry-run", "", None):
                it.pop("status", None)
                items.append(it)
        log("reuse manifest: %d candidates loaded from %s" % (len(items), args.reuse_manifest))

    for feed in ([] if args.reuse_manifest else conf.get("feeds", [])):
        name, url = feed["name"], feed["url"]
        try:
            body, ctype, final = pol.fetch(url, 3 * 1024 * 1024)
            parsed = feedparser.parse(body)
            if not parsed.entries:
                # 站点换了 feed 地址 / 直接返回 HTML：尝试从页面里自动发现 feed
                alt = discover_feed_url(body.decode("utf-8", "replace"), final)
                if alt and alt != url:
                    try:
                        body, ctype, final = pol.fetch(alt, 3 * 1024 * 1024)
                        parsed = feedparser.parse(body)
                        if parsed.entries:
                            log("  [discover] %s -> %s" % (name, alt))
                    except Exception as e:
                        log("  [discover-fail] %s -> %s (%s)" % (name, alt, type(e).__name__))
            if not parsed.entries:
                log("  [skip] %s feed parse failed: %s" % (name, str(parsed.get("bozo_exception"))[:120]))
                continue
            n_new = 0
            for e in parsed.entries[:40]:
                link = urllib.parse.urljoin(final, (e.get("link") or "").strip())
                if not link or link in seen:
                    continue
                dt = entry_date(e)
                if dt and dt < cutoff:
                    continue
                title = re.sub(r"\s+", " ", e.get("title") or "").strip()
                summary = strip_html(e.get("summary") or e.get("description") or "", 1500)
                sc = score_entry(title, summary, feed.get("trust", 0.0))
                rec = {
                    "source": name,
                    "feed_category": feed.get("category", "杂项"),
                    "url": link,
                    "title": title,
                    "published": dt.astimezone(CST).strftime("%Y-%m-%d") if dt else "",
                    "summary": summary,
                    "score": sc["score"],
                    "signals": {k: sc[k] for k in ("domain", "novelty", "depth", "negative")},
                    "category": infer_category(title + " " + summary, feed.get("category", "杂项")),
                }
                items.append(rec)
                n_new += 1
            log("  %-24s ok, new %d" % (name, n_new))
        except PermissionError as e:
            log("  [robots] %s -> %s" % (name, str(e)[:100]))
        except Exception as e:
            log("  [fail] %s: %s" % (name, type(e).__name__ + " " + str(e)[:120]))

    items.sort(key=lambda x: x["score"], reverse=True)
    shortlist = [i for i in items if i["score"] >= args.min_score and is_relevant(i["signals"])]
    log("candidates %d, above threshold %.1f: %d" % (len(items), args.min_score, len(shortlist)))

    manifest = {"week": week, "generated": now.isoformat(), "lookback_days": args.days,
                "feeds": len(conf.get("feeds", [])), "candidates": len(items),
                "shortlist": len(shortlist), "items": []}

    downloaded = 0
    used_bytes = 0
    for idx, rec in enumerate(shortlist, start=1):
        if downloaded >= max_fetch:
            log("download limit %d reached, stop" % max_fetch)
            break
        if used_bytes >= run_budget:
            log("download byte budget %.1f MB reached, stop" % (run_budget / 1048576.0))
            break
        if args.dry_run:
            rec["status"] = "dry-run"
            manifest["items"].append(rec)
            continue
        try:
            body, ctype, final = pol.fetch(rec["url"], max_article_bytes + 400000)
        except PermissionError:
            rec["status"] = "robots-blocked"
            log("  [robots] skip %s" % rec["url"])
            manifest["items"].append(rec)
            continue
        except Exception as e:
            rec["status"] = "fetch-error"
            log("  [fail] %s (%s)" % (rec["url"], type(e).__name__))
            manifest["items"].append(rec)
            continue

        if "pdf" in ctype.lower() or body[:4] == b"%PDF":
            rec["status"] = "pdf-skipped"
            log("  [pdf] skip %s" % rec["url"])
            manifest["items"].append(rec)
            continue

        text = extract_main_text(body.decode("utf-8", "replace"), final)
        if len(text) < 800:
            text = extract_main_text(body.decode("gb18030", "replace"), final)
        if len(text) < 800:
            text = extract_from_embedded_json(body.decode("utf-8", "replace"))
        link_only = False
        if len(text) < 800:
            # 前端渲染 / 正文抓不到：仍然保留元数据 + 摘要，标记 link-only
            text = (rec.get("summary") or "").strip()
            link_only = True
            if len(text) < 40:
                rec["status"] = "extract-failed"
                log("  [short] %s" % rec["url"])
                manifest["items"].append(rec)
                continue
            log("  [link-only] %s" % rec["url"])

        truncated = False
        if len(text.encode("utf-8")) > max_article_bytes:
            text = text.encode("utf-8")[:max_article_bytes].decode("utf-8", "ignore")
            text += "\n\n---\n\n_[snapshot truncated at " + human_size(max_article_bytes) + ", see original]_\n"
            truncated = True

        rec["category"] = infer_category(rec["title"] + " " + text[:4000],
                                          rec.get("feed_category") or rec["category"])

        sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        size = len(text.encode("utf-8"))
        used_bytes += len(body)
        downloaded += 1

        fname = "%02d-%s.md" % (idx, slugify(rec["title"]))
        keywords = rec["signals"]["novelty"][:4] + rec["signals"]["domain"][:4]
        fm = [
            "---",
            "title: " + json.dumps(rec["title"], ensure_ascii=False),
            "source: " + json.dumps(rec["source"], ensure_ascii=False),
            "url: " + rec["url"],
            "published: " + rec["published"],
            "fetched: " + now.isoformat(),
            "category: " + json.dumps(rec["category"], ensure_ascii=False),
            "score: " + str(rec["score"]),
            "keywords: " + json.dumps(keywords, ensure_ascii=False),
            "sha256: " + sha,
            "bytes: " + str(size),
            "truncated: " + ("true" if truncated else "false"),
            "body_mode: " + ("link-only" if link_only else "fulltext"),
            "status: candidate",
            "---",
            "",
            "# " + rec["title"],
            "",
            "> 来源：" + rec["source"] + " · " + rec["published"] + " · [原文](" + rec["url"] + ")",
            "> 自动抓取快照，仅供安全研究参考；版权归原作者所有。",
            "",
        ]
        if link_only:
            fm.extend(["> ⚠️ 原文页面为前端渲染，正文未能完整抓取；此处仅保留摘要，请阅读原文。", ""])
        with open(os.path.join(staging, fname), "w", encoding="utf-8") as f:
            f.write("\n".join(fm) + "\n" + text + "\n")

        rec.update(status="staged", file=fname, bytes=size, sha256=sha, truncated=truncated)
        manifest["items"].append(rec)
        seen[rec["url"]] = {"first_seen": now.isoformat(), "sha256": sha, "file": fname}
        log("  [%d] %s  score=%.1f  %s" % (downloaded, human_size(size), rec["score"], rec["title"][:70]))

    if args.dry_run:
        recorded = set(i.get("url") for i in manifest["items"])
        for it in items:
            if it["url"] not in recorded:
                it = dict(it)
                it["status"] = "below-threshold"
                manifest["items"].append(it)
        manifest["items"].sort(key=lambda x: x["score"], reverse=True)

    manifest["downloaded"] = downloaded
    manifest["requests"] = pol.requests_made
    manifest["downloaded_bytes"] = used_bytes
    save_json(os.path.join(staging, "manifest.json"), manifest)

    head = [
        "# 本周候选（待复审） " + week,
        "",
        "- 生成时间：" + now.strftime("%Y-%m-%d %H:%M"),
        "- 回溯 " + str(args.days) + " 天 | feed " + str(len(conf.get("feeds", []))) + " 个 | 候选 "
        + str(len(items)) + " 条 | 达标 " + str(len(shortlist)) + " 条 | 本次下载 " + str(downloaded)
        + " 篇（" + human_size(used_bytes) + "）| 请求 " + str(pol.requests_made) + " 次",
        "",
        "> 复审标准：**攻击角度新颖** 或 **利用难度极高**；只保留有研究价值的漏洞/技术文章。",
        "> 发布：python tools/publish.py --week " + week + " --pick 01,03,05  （编号见下表）",
        "",
        "| # | 分数 | 抓取 | 分类 | 标题 | 来源 | 日期 |",
        "|---|------|------|------|------|------|------|",
    ]
    for rec in manifest["items"]:
        num = rec.get("file", "")[:2] if rec.get("file") else "-"
        flag = "OK" if rec.get("status") == "staged" else rec.get("status", "-")
        row = ["", num, "%.1f" % rec["score"], flag, rec["category"],
               "[" + rec["title"].replace("|", "/") + "](" + rec["url"] + ")",
               rec["source"], rec["published"], ""]
        head.append("|".join(row))
    head.append("")

    details = []
    for rec in manifest["items"]:
        if rec.get("status") != "staged":
            continue
        details.append("## " + rec["file"][:2] + " · " + rec["title"])
        details.append("")
        details.append("- 原文：" + rec["url"])
        details.append("- 命中：新颖 " + (", ".join(rec["signals"]["novelty"]) or "-")
                       + " / 领域 " + (", ".join(rec["signals"]["domain"]) or "-")
                       + " / 深度 " + (", ".join(rec["signals"]["depth"]) or "-"))
        details.append("- 摘要：" + (rec["summary"][:400] or "-"))
        details.append("")

    with open(os.path.join(staging, "candidates.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(head + details) + "\n")

    state["seen"] = seen
    state.setdefault("runs", []).append({
        "week": week, "at": now.isoformat(), "candidates": len(items),
        "shortlist": len(shortlist), "downloaded": downloaded, "bytes": used_bytes,
    })
    state["runs"] = state["runs"][-52:]
    save_json(STATE_PATH, state)

    log("done: candidates %d / shortlist %d / downloaded %d / %s -> %s"
        % (len(items), len(shortlist), downloaded, human_size(used_bytes),
           os.path.relpath(staging, ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
