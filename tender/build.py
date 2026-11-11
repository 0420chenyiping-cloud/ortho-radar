"""骨科招采雷达：把 data/ 下的 JSON 嵌入 template.html，生成单文件 index.html。

用法：python3 build.py
data/items.json      逐条发文与公告（数组）
data/provinces.json  各省执行状态矩阵 {"columns": [...], "rows": [...]}
data/meta.json       更新日期、本期摘要、检索盲区、竞品关键词
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
LEVELS = {"国家", "联采办", "省际联盟", "省", "地市", "医院"}
TYPES = {"政策", "集采节点", "挂网价格", "招标", "中标"}
CATS = {"创伤", "脊柱", "关节", "运动医学", "CMF", "骨科机器人", "高值耗材通用"}
SOURCES = {"官方原文", "官方原文（未能打开）", "官方转发", "官方媒体", "转载线索"}
KEYS = {"id", "date", "added", "level", "org", "province", "city", "type", "stage", "categories",
        "title", "summary", "key_dates", "winners", "pinned", "source_type", "source_name", "url"}
DATE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")


def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def fail(msg):
    sys.exit("数据校验失败：" + msg)


def check_items(items, provinces):
    ids = set()
    for r in items:
        rid = r.get("id")
        missing = KEYS - r.keys()
        if missing:
            fail(f"{rid} 缺字段 {sorted(missing)}")
        if rid in ids:
            fail(f"id 重复 {rid}")
        ids.add(rid)
        if r["level"] not in LEVELS:
            fail(f"{rid} 层级不合法：{r['level']}")
        if r["type"] not in TYPES:
            fail(f"{rid} 类型不合法：{r['type']}")
        if not r["categories"] or any(c not in CATS for c in r["categories"]):
            fail(f"{rid} 产品线不合法：{r['categories']}")
        if r["source_type"] not in SOURCES:
            fail(f"{rid} 来源标注不合法：{r['source_type']}")
        if r["province"] != "全国" and r["province"] not in provinces:
            fail(f"{rid} 省份不在 31 省名单里：{r['province']}")
        for d in [r["date"], r["added"]] + [k.get("date", "") for k in r["key_dates"]]:
            if not DATE.match(str(d)):
                fail(f"{rid} 日期格式不对：{d}")
        if not str(r["url"]).startswith(("http://", "https://")):
            fail(f"{rid} 链接不是网址：{r['url']}")


def main():
    items, prov, meta = load("items.json"), load("provinces.json"), load("meta.json")
    names = {r["province"] for r in prov["rows"]}
    if len(names) != 31:
        fail(f"省份矩阵应为 31 行，现在是 {len(names)}")
    check_items(items, names)
    payload = json.dumps({"meta": meta, "items": items, "provinces": prov}, ensure_ascii=False).replace("</", "<\\/")
    html = (ROOT / "template.html").read_text(encoding="utf-8")
    if "/*__DATA__*/" not in html:
        fail("template.html 里找不到数据占位符")
    (ROOT / "index.html").write_text(html.replace("/*__DATA__*/", payload), encoding="utf-8")
    pinned = sum(1 for r in items if r["pinned"])
    print(f"index.html 已生成：{len(items) - pinned} 条 + 背景政策 {pinned} 条，更新于 {meta.get('updated', '')}")


if __name__ == "__main__":
    main()
