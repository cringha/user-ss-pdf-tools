#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
北京社保PDF（多险种分行格式）人员信息提取与截图生成
- 提取所有人员姓名（基于“序号 姓名 身份证号”模式）
- 为每个人在输出目录下创建子目录
- 为每个包含该人员的页面生成截图，并用红色矩形框标出该人员所占的所有行
"""

import re
import io
import os
import argparse
from collections import defaultdict
from typing import List, Tuple, Optional, Dict, Set

import fitz  # PyMuPDF
import pdfplumber
from PIL import Image, ImageDraw


# ================== 1. 提取所有人员姓名 ==================
def extract_names_from_pdf(pdf_path: str) -> List[str]:
    """
    提取北京社保格式中的所有人员姓名（保持出现顺序，去重）
    匹配行模式：数字 + 姓名 + 身份证号（同在一行）
    """
    # 匹配：行首可选空格 + 数字 + 中文姓名(2~4字) + 空格 + 身份证号(15/18位)
    pattern = re.compile(r"^\s*(\d+)\s+([\u4e00-\u9fa5]{2,4})\s+(\d{15,18})")
    names = []
    seen = set()
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.split("\n"):
                line = line.strip()
                m = pattern.match(line)
                if m:
                    name = m.group(2)
                    # 过滤明显不是人名的词
                    if (
                        name not in {"序号", "姓名", "社会保障号码"}
                        and name not in seen
                    ):
                        seen.add(name)
                        names.append(name)
    if not names:
        raise ValueError("未提取到任何有效人员姓名，请检查PDF是否为北京社保格式。")
    return names


# ================== 2. 获取页面上所有行的边界框 ==================
def get_lines_on_page(
    page_obj: pdfplumber.page.Page, y_tolerance: float = 5.0
) -> List[dict]:
    """
    提取页面上所有文本行，每行包含 {'text': str, 'bbox': (x0, top, x1, bottom)}
    """
    words = page_obj.extract_words(
        keep_blank_chars=False,
        use_text_flow=True,
        extra_attrs=["text", "x0", "top", "x1", "bottom"],
    )
    if not words:
        return []
    # 转换为标准格式
    words_list = []
    for w in words:
        words_list.append(
            {
                "text": w["text"],
                "x0": w["x0"],
                "top": w["top"],
                "x1": w["x1"],
                "bottom": w["bottom"],
            }
        )
    # 按top排序
    words_list.sort(key=lambda w: (w["top"], w["x0"]))

    # 聚类成行
    lines = []
    current_line = [words_list[0]]
    current_top = words_list[0]["top"]
    for w in words_list[1:]:
        if abs(w["top"] - current_top) <= y_tolerance:
            current_line.append(w)
        else:
            lines.append(_merge_line(current_line))
            current_line = [w]
            current_top = w["top"]
    if current_line:
        lines.append(_merge_line(current_line))
    return lines


def _merge_line(words: List[dict]) -> dict:
    """合并一行内的单词，返回合并文本和整体bbox"""
    text = "".join(w["text"] for w in words)
    x0 = min(w["x0"] for w in words)
    top = min(w["top"] for w in words)
    x1 = max(w["x1"] for w in words)
    bottom = max(w["bottom"] for w in words)
    return {"text": text, "bbox": (x0, top, x1, bottom)}


# ================== 3. 定位某人员在页面上的全部行区域 ==================
def find_person_bbox_on_page(
    page_obj: pdfplumber.page.Page, person_name: str
) -> Optional[Tuple[float, float, float, float]]:
    """
    返回人员在该页面上的整体边界框 (x0, top, x1, bottom)
    从包含姓名的“序号 姓名 身份证号”行开始，向下到下一个人员序号行之前或页尾。
    """
    lines = get_lines_on_page(page_obj)
    # 找出所有包含该姓名的行（通常只有一行是序号行）
    name_lines_idx = [i for i, line in enumerate(lines) if person_name in line["text"]]
    if not name_lines_idx:
        return None
    # 取第一个匹配行作为起始行
    start_idx = name_lines_idx[0]
    # 寻找结束行：从start_idx+1开始，找到第一个匹配 r'^\s*\d+\s+' 的行（下一个人员序号行）
    end_idx = start_idx
    next_person_pattern = re.compile(r"^\s*\d+\s+[\u4e00-\u9fa5]{2,4}\s+\d{15,18}")
    for i in range(start_idx + 1, len(lines)):
        line_text = lines[i]["text"].strip()
        if next_person_pattern.match(line_text):
            break
        end_idx = i
    # 计算整体bbox：取start_idx到end_idx所有行的最小x0、最大x1、最小top、最大bottom
    bbox_list = [lines[i]["bbox"] for i in range(start_idx, end_idx + 1)]
    x0 = min(b[0] for b in bbox_list)
    top = min(b[1] for b in bbox_list)
    x1 = max(b[2] for b in bbox_list)
    bottom = max(b[3] for b in bbox_list)
    return (x0, top, x1, bottom)


# ================== 4. 生成截图并画框 ==================
def render_page_with_rect(
    pdf_path: str,
    page_num: int,
    bbox: Tuple[float, float, float, float],
    zoom: float = 2.0,
    output_path: str = None,
) -> None:
    """
    渲染PDF页面为PNG，并在指定bbox画红色矩形框（线宽3）
    """
    doc = fitz.open(pdf_path)
    page = doc[page_num]  # 0-based
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data))

    # bbox 坐标转换（PDF点 → 像素）
    x0, y0, x1, y1 = bbox
    px0 = x0 * zoom
    py0 = y0 * zoom
    px1 = x1 * zoom
    py1 = y1 * zoom

    draw = ImageDraw.Draw(img)
    draw.rectangle([px0, py0, px1, py1], outline="red", width=3)
    img.save(output_path, "PNG")
    doc.close()


def generate_screenshots_for_person(
    pdf_path: str, person_name: str, output_root: str, zoom: float = 2.0
) -> None:
    """
    为单个人生成所有相关页面的截图（保存到 output_root/person_name/）
    """
    person_dir = os.path.join(output_root, person_name)
    os.makedirs(person_dir, exist_ok=True)

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            bbox = find_person_bbox_on_page(page, person_name)
            if bbox:
                out_file = os.path.join(
                    person_dir, f"{person_name}_第{page_idx + 1}页.png"
                )
                render_page_with_rect(pdf_path, page_idx, bbox, zoom, out_file)
                print(f"  -> {out_file}")


PDF_PATH = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\北京60人.pdf"


# ================== 5. 主程序 ==================
def main():
    parser = argparse.ArgumentParser(
        description="北京社保PDF人员信息提取与截图（多险种分行格式）"
    )
    # parser.add_argument("pdf_file", help="PDF文件路径")
    parser.add_argument("--output", "-o", default="./社保截图输出", help="输出根目录")
    parser.add_argument(
        "--zoom", type=float, default=2.0, help="截图放大倍数（默认2.0）"
    )
    args = parser.parse_args()

    # pdf_path = args.pdf_file

    pdf_path = PDF_PATH
    if not os.path.exists(pdf_path):
        print(f"错误：文件不存在 {pdf_path}")
        return

    print(f"正在处理：{pdf_path}")
    # 提取姓名
    names = extract_names_from_pdf(pdf_path)
    print(f"共提取 {len(names)} 人：{', '.join(names)}")

    # 为每个人生成截图
    for idx, name in enumerate(names, 1):
        print(f"[{idx}/{len(names)}] 处理 {name} ...")
        generate_screenshots_for_person(pdf_path, name, args.output, args.zoom)

    print(f"\n全部完成！截图保存在：{args.output}")
    # 生成人员清单
    with open(os.path.join(args.output, "人员清单.txt"), "w", encoding="utf-8") as f:
        for name in names:
            f.write(f"{name}\n")


if __name__ == "__main__":
    main()
