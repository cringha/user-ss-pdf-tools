#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
成都社保PDF人员信息提取（改进版）
- 使用正则搜索整页文本，匹配“序号 身份证号 姓名”模式
- 过滤非中文人名（2~4个汉字）
- 输出去重后的人员名单及完整记录
"""

import re
import pandas as pd
import pdfplumber
from typing import List, Dict

PDF_PATH = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\成都.pdf"


def is_valid_name(name: str) -> bool:
    """判断是否为有效中文人名（2~4个汉字，排除表头等）"""
    if not isinstance(name, str):
        return False
    name = name.strip()
    if not re.fullmatch(r"[\u4e00-\u9fa5]{2,4}", name):
        return False
    # 排除常见非人名词
    blacklist = {
        "序号",
        "姓名",
        "证件号码",
        "养老保险",
        "失业保险",
        "工伤保险",
        "企业职工养老",
        "缴费情况",
        "查询专用章",
        "单位名称",
        "打印时间",
        "说明",
        "验证码",
        "有效期",
        "欠费情况",
        "人员缴费信息",
    }
    if name in blacklist:
        return False
    return True


def extract_person_records(pdf_path: str) -> List[Dict]:
    """
    提取所有“序号 身份证号 姓名”组合
    使用正则搜索整页文本，避免逐行匹配遗漏
    """
    # 匹配模式：序号（数字） + 空格/换行 + 身份证号(15/18位) + 空格/换行 + 中文姓名(2~4字)
    pattern = re.compile(r"(\d+)\s+(\d{15,18})\s+([\u4e00-\u9fa5]{2,4})")
    records = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            # 在整页文本中搜索所有匹配项
            for match in pattern.finditer(text):
                seq, id_num, name = match.groups()
                if is_valid_name(name):
                    records.append({"序号": int(seq), "证件号码": id_num, "姓名": name})
    # 按序号排序（以防乱序）
    records.sort(key=lambda x: x["序号"])
    return records


def main():
    pdf_file = PDF_PATH  # "成都.pdf"  # 可修改为实际路径
    try:
        records = extract_person_records(pdf_file)
        if not records:
            print("未提取到任何有效记录，请检查PDF格式。")
            return

        df = pd.DataFrame(records)
        # 按序号排序（已排序，但保险）
        df = df.sort_values("序号").reset_index(drop=True)

        print(f"成功提取 {len(df)} 条记录：")
        print(df.to_string(index=False))

        # 保存完整记录
        output_csv = "成都_社保人员信息.csv"
        df.to_csv(output_csv, index=False, encoding="utf-8-sig")
        print(f"\n完整记录已保存至：{output_csv}")

        # 输出唯一人员名单
        unique_names = df["姓名"].unique()
        print(f"\n共有 {len(unique_names)} 名不同人员：")
        print(", ".join(unique_names))

        # 仅保存人员名单
        pd.DataFrame({"姓名": unique_names}).to_csv(
            "成都_人员名单.csv", index=False, encoding="utf-8-sig"
        )

    except Exception as e:
        print(f"错误：{e}")


if __name__ == "__main__":
    main()
