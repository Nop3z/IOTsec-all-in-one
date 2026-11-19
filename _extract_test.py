
import sys, os, re
sys.path.insert(0, os.path.join(os.getcwd(), "tools"))
import crawl
from bs4 import BeautifulSoup

pol = crawl.Politeness({"proxy":"http://127.0.0.1:10810","timeout_sec":30,"request_min_interval_sec":1})
url = "https://eclypsium.com/blog/cron-persistence-network-appliances/"
body, ctype, final = pol.fetch(url, 600000)
html = body.decode("utf-8","replace")
soup = BeautifulSoup(html, "lxml")
for t in soup(list(crawl.DROP_TAGS)):
    t.decompose()
best = []
for node in soup.find_all(["article","main","div","section"]):
    ps = node.find_all("p", recursive=True)
    score = sum(len(p.get_text(" ", strip=True)) for p in ps)
    if score > 400:
        best.append((score, node))
best.sort(key=lambda x: -x[0])
print("top candidates:", len(best))
for score, node in best[:3]:
    txt = node.get_text(" ", strip=True)
    print("--- score", score, "tag", node.name, "class", node.get("class"), "len", len(txt))
    print(txt[:200].replace("\n"," "))
md = crawl.md_block(best[0][1], final) if best else ""
md = re.sub(r"\n{3,}", "\n\n", md).strip()
print("\n=== md len:", len(md))
print(md[:600])
