#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
社保PDF人员信息提取与截图生成工具
- 从PDF中提取所有参保人员姓名（基于“序号+姓名+身份证号”模式）
- 为每位人员在指定输出目录下创建以姓名命名的子目录
- 对每个包含该人员的PDF页面，生成完整页面截图，并用红色矩形框标出该人员所在行
- 截图包含企业名称、公章等页面全部信息
"""

import io
import re
import os
import argparse
from collections import defaultdict
from typing import List, Tuple, Optional

import fitz  # PyMuPDF
import pdfplumber
from PIL import Image, ImageDraw


# ================== 姓名提取模块 ==================
def extract_names_from_pdf(pdf_path: str) -> List[str]:
    """
    从PDF中提取所有有效人员姓名（按出现顺序，去重）
    匹配模式：行首可选空格 + 数字 + 中文姓名(2-4字) + 身份证号(15/18位)
    """
    name_pattern = re.compile(
        r"^\s*(\d+)\s+"  # 序号
        r"([\u4e00-\u9fa5]{2,4})\s+"  # 姓名（2~4汉字）
        r"(\d{15,18})"  # 身份证号
    )
    names = []
    seen = set()

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.split("\n"):
                line = line.strip()
                match = name_pattern.match(line)
                if match:
                    name = match.group(2)
                    # 过滤明显不是人名的关键词
                    if name not in {"序号", "姓名", "身份证号", "个人编号", "单位名称"}:
                        if name not in seen:
                            seen.add(name)
                            names.append(name)
    if not names:
        raise ValueError("未从PDF中提取到任何有效人员姓名，请检查PDF格式。")
    return names


# ================== 页面内人员行定位模块 ==================
def get_word_bboxes(page_obj: pdfplumber.page.Page) -> List[dict]:
    """提取页面上所有单词及其边界框，并附加文本"""
    words = page_obj.extract_words(
        keep_blank_chars=False,
        use_text_flow=True,
        extra_attrs=["text", "x0", "top", "x1", "bottom"],
    )
    # 统一转换为标准字段名
    result = []
    for w in words:
        result.append(
            {
                "text": w["text"],
                "x0": w["x0"],
                "top": w["top"],
                "x1": w["x1"],
                "bottom": w["bottom"],
            }
        )
    return result


def group_words_into_lines(words: List[dict], y_tolerance: float = 5.0) -> List[dict]:
    """
    将单词按垂直位置（top）聚类为行
    返回每行的字典：{'text': '合并的文本', 'bbox': (x0, top, x1, bottom)}
    """
    if not words:
        return []
    # 按top排序
    sorted_words = sorted(words, key=lambda w: (w["top"], w["x0"]))
    lines = []
    current_line = [sorted_words[0]]
    current_top = sorted_words[0]["top"]

    for word in sorted_words[1:]:
        # 如果单词的top与当前行顶部相差在容忍范围内，归为同一行
        if abs(word["top"] - current_top) <= y_tolerance:
            current_line.append(word)
        else:
            # 完成当前行
            lines.append(merge_line_words(current_line))
            current_line = [word]
            current_top = word["top"]
    if current_line:
        lines.append(merge_line_words(current_line))
    return lines


def merge_line_words(words_in_line: List[dict]) -> dict:
    """将一行中的单词合并，并计算整体bbox"""
    text = "".join(w["text"] for w in words_in_line)
    x0 = min(w["x0"] for w in words_in_line)
    top = min(w["top"] for w in words_in_line)
    x1 = max(w["x1"] for w in words_in_line)
    bottom = max(w["bottom"] for w in words_in_line)
    return {"text": text, "bbox": (x0, top, x1, bottom)}


def find_person_row_on_page(
    pdfplumber_page, person_name: str
) -> Optional[Tuple[float, float, float, float]]:
    """
    在给定pdfplumber页面上查找人员姓名所在行的边界框
    返回 (x0, top, x1, bottom) 或 None
    """
    words = get_word_bboxes(pdfplumber_page)
    lines = group_words_into_lines(words)
    for line in lines:
        if person_name in line["text"]:
            return line["bbox"]
    return None


# ================== 截图与画框模块 ==================
def render_page_and_draw_rect(
    pdf_path: str,
    page_num: int,
    bbox: Tuple[float, float, float, float],
    zoom: float = 2.0,
    output_path: str = None,
) -> None:
    """
    使用PyMuPDF渲染PDF页面为图像，在指定bbox处绘制红色矩形框，并保存为PNG
    bbox: (x0, y0, x1, y1) 页面原始坐标系（点为单位）
    zoom: 渲染缩放倍数，越大图像越清晰
    """
    # 打开PDF
    doc = fitz.open(pdf_path)
    page = doc[page_num]  # 0-based
    # 计算变换矩阵
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img_data = pix.tobytes("png")
    # img = Image.open(pix.tobytes("png"))  # 直接用bytes打开

    img = Image.open(io.BytesIO(img_data))  # 修正这里

    # 转换bbox到图像坐标系
    x0, y0, x1, y1 = bbox
    img_x0 = x0 * zoom
    img_y0 = y0 * zoom
    img_x1 = x1 * zoom
    img_y1 = y1 * zoom
    # 在图像上画红色矩形框（线宽3）
    draw = ImageDraw.Draw(img)
    draw.rectangle([img_x0, img_y0, img_x1, img_y1], outline="red", width=3)
    # 保存
    if output_path:
        img.save(output_path, "PNG")
    else:
        img.save("temp.png", "PNG")  # fallback
    doc.close()


def generate_screenshots_for_person(
    pdf_path: str, person_name: str, output_dir: str, zoom: float = 2.0
) -> None:
    """
    为单个人员生成所有相关页面的截图，保存到 output_dir/person_name/ 下
    截图文件名：人名_第N页.png
    """
    # 创建个人子目录
    person_folder = os.path.join(output_dir, person_name)
    os.makedirs(person_folder, exist_ok=True)

    with pdfplumber.open(pdf_path) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            bbox = find_person_row_on_page(page, person_name)
            if bbox:
                # 构造输出文件名
                output_file = os.path.join(
                    person_folder, f"{person_name}_第{page_idx + 1}页.png"
                )
                render_page_and_draw_rect(
                    pdf_path, page_idx, bbox, zoom=zoom, output_path=output_file
                )
                print(f"  -> 已生成截图: {output_file}")


PDF_PATH = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\武汉.pdf"


# ================== 主程序 ==================
def main():
    parser = argparse.ArgumentParser(description="社保PDF人员信息提取与截图生成")
    # parser.add_argument("pdf_file", help="PDF文件路径", default=PDF_PATH)
    parser.add_argument(
        "--output",
        "-o",
        default="./社保截图输出",
        help="输出根目录（默认为 ./社保截图输出）",
    )
    parser.add_argument(
        "--zoom",
        type=float,
        default=2.0,
        help="截图放大倍数，越高越清晰但文件越大（默认2.0）",
    )
    args = parser.parse_args()

    pdf_path = PDF_PATH  # args.pdf_file
    output_root = args.output
    zoom = args.zoom

    if not os.path.exists(pdf_path):
        print(f"错误：PDF文件不存在 - {pdf_path}")
        return

    print(f"正在处理 PDF: {pdf_path}")
    # 1. 提取所有人员姓名
    names = extract_names_from_pdf(pdf_path)
    print(f"共提取到 {len(names)} 名人员: {', '.join(names)}")

    # 2. 为每位人员生成截图
    for idx, name in enumerate(names, 1):
        print(f"[{idx}/{len(names)}] 正在处理: {name}")
        generate_screenshots_for_person(pdf_path, name, output_root, zoom)

    print(f"\n全部完成！截图保存在: {output_root}")
    # 可选：生成汇总清单
    with open(os.path.join(output_root, "人员清单.txt"), "w", encoding="utf-8") as f:
        for name in names:
            f.write(f"{name}\n")
    print(f"人员清单已保存: {os.path.join(output_root, '人员清单.txt')}")


if __name__ == "__main__":
    main()
