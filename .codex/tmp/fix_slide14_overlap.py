from __future__ import annotations

import os
import re
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.etree import ElementTree as ET


SRC = Path(os.environ["PPT_SOURCE"])
OUT = Path(os.environ["PPT_OUTPUT"])

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


REPLACEMENTS = {
    "按照项目流程呈现成员分工，说明 GitHub 提交包中各模块的主要责任与支持关系。": "按项目流程呈现分工，说明各模块责任与最终成果对应。",
    "• 高俊杰：组长，负责主题确定、课程要求拆解、仓库结构、README、课程论文、PPT 归档与最终巡检。\n": "• 高俊杰：统筹选题、仓库结构、README、论文与最终巡检。\n",
    "• 重点整合：数据来源、筛选流程、RQ、三图一表、高被引文献表、图表解释和可复现说明。\n": "• 重点整合：数据来源、RQ、三图一表、图表解释与复现说明。\n",
    "• 最终提交：paper / presentation / reflection / reports 等材料统一检查与归档。\n": "• 最终归档：paper / presentation / reflection / reports。\n",
    "• 赵世铎：协助 Lens.org 检索策略、关键词组合、原始数据导出和检索口径记录。\n": "• 赵世铎：协助 Lens.org 检索、关键词组合与原始数据导出。\n",
    "• 解明昊：协助 DOI / Title 去重、字段完整性检查和 M1 数据质量报告整理。\n": "• 解明昊：协助 DOI / Title 去重、字段检查与 M1 质量报告。\n",
    "• 产出支撑：config/query.yaml、data/raw、data/processed、screening_records 与数据质量说明。\n": "• 支撑文件：query.yaml、raw/processed 数据与筛选记录。\n",
    "• 杨广宸：协助年度趋势、关键词共现、作者合作、机构/国家、引用与共被引网络分析。\n": "• 杨广宸：协助趋势、关键词、合作网络与共被引分析。\n",
    "• 罗博伟：协助 milestone 文献筛选、mini review 主题线索、挑战与未来方向整理。\n": "• 罗博伟：协助 milestone 文献、综述主线与挑战方向整理。\n",
    "• 产出支撑：outputs/figures、review_figures、milestone candidates、M2/M3 报告。\n": "• 支撑文件：figures、review_figures、milestone 与 M2/M3 报告。\n",
    "按文献计量项目流程拆分：检索 → 清洗 → 计量分析 → 综述写作 → GitHub 归档。": "按流程拆分：检索 → 清洗 → 计量分析 → 综述写作 → GitHub 归档。",
    "README、reports、paper、presentation、reflection 中均保留分工说明与个人反思材料，便于课程检查。": "README、reports、paper、presentation、reflection 均保留对应成果。",
    "小组分工与个人反思已归档至 reflection/，作为个人贡献说明与差异化评分参考。": "小组分工与个人反思已归档至 reflection/，便于个人贡献核查。",
}


def main() -> None:
    if not SRC.exists():
        raise FileNotFoundError(SRC)

    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "pptx"
        with ZipFile(SRC, "r") as zin:
            zin.extractall(root)

        slide = root / "ppt" / "slides" / "slide14.xml"
        tree = ET.parse(slide)
        sroot = tree.getroot()
        for t in sroot.findall(".//a:t", NS):
            if t.text in REPLACEMENTS:
                t.text = REPLACEMENTS[t.text]
            elif t.text:
                t.text = re.sub(r"(\b0?\d{1,2})/14\b", lambda m: "14/14" if m.group(1) == "14" else m.group(0), t.text)

        tree.write(slide, encoding="utf-8", xml_declaration=True)

        if OUT.exists():
            OUT.unlink()
        with ZipFile(OUT, "w", ZIP_DEFLATED) as zout:
            for path in root.rglob("*"):
                if path.is_file():
                    zout.write(path, path.relative_to(root).as_posix())

    print(OUT)


if __name__ == "__main__":
    main()
