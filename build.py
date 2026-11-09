"""把 data/ 下的 JSON 嵌入 template.html，生成单文件 index.html。

用法：python3 build.py
data/solutions.json  近 6 个月新方案（数组）
data/pains.json      痛点与热点（数组）
data/meta.json       {"updated": "YYYY-MM-DD"}
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
LINES = {"创伤", "脊柱", "关节", "运动医学", "CMF"}
SOL_KEYS = {"id", "line", "date", "product", "company", "region", "event", "what", "pain",
            "pain_basis", "source_tier", "source_name", "url"}
PAIN_KEYS = {"id", "line", "kind", "title", "detail", "basis", "source_name", "url"}


def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def check(rows, keys, label):
    ids = set()
    for r in rows:
        missing = keys - r.keys()
        if missing:
            sys.exit(f"{label} {r.get('id')} 缺字段：{sorted(missing)}")
        if r["line"] not in LINES:
            sys.exit(f"{label} {r['id']} 的产线不在五条之内：{r['line']}")
        if r["id"] in ids:
            sys.exit(f"{label} id 重复：{r['id']}")
        ids.add(r["id"])


def main():
    sol, pains, meta = load("solutions.json"), load("pains.json"), load("meta.json")
    check(sol, SOL_KEYS, "方案")
    check(pains, PAIN_KEYS, "痛点")
    payload = json.dumps({"updated": meta.get("updated", ""), "solutions": sol, "pains": pains},
                         ensure_ascii=False).replace("</", "<\\/")
    html = (ROOT / "template.html").read_text(encoding="utf-8")
    if "/*__DATA__*/" not in html:
        sys.exit("template.html 里找不到数据占位符")
    (ROOT / "index.html").write_text(html.replace("/*__DATA__*/", payload), encoding="utf-8")
    print(f"index.html 已生成：{len(sol)} 项方案，{len(pains)} 条痛点/热点，更新于 {meta.get('updated', '')}")


if __name__ == "__main__":
    main()
