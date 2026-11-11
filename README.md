# 骨科临床雷达

创伤、脊柱、关节、运动医学、CMF 五条产线的临床痛点、行业热点与近 6 个月全球骨科新方案。每周一由 Claude 检索更新。

## 文件

- `data/solutions.json`：近 6 个月新方案
- `data/pains.json`：临床痛点与行业热点
- `data/meta.json`：数据更新日期
- `template.html`：页面模板
- `build.py`：把数据嵌入模板，生成 `index.html`（`python3 build.py`）
- `index.html`：发布的页面，单文件，可直接用浏览器打开

资料整理自公开来源，仅供行业研究参考。

## 骨科招采雷达（tender/）

骨科及骨科手术机器人的医保政策、集采节点、挂网价格、招标中标信息，按国家 → 联采办 → 省际联盟 → 省 → 地市 → 医院逐层汇总，每周一、四更新。

- `tender/data/items.json`：逐条发文与公告
- `tender/data/provinces.json`：各省执行状态矩阵
- `tender/data/meta.json`：更新日期、本期摘要、检索盲区、竞品关键词
- `tender/build.py`：校验数据并生成 `tender/index.html`
