#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
成都社保PDF人员信息提取（基于表格解析）
- 使用 pdfplumber 的 extract_tables() 提取表格数据
- 从每行中提取“序号”、“证件号码”、“姓名”
- 过滤非中文人名（2~4个汉字）
- 输出去重后的人员名单及完整记录
"""

import re
import pandas as pd
import pdfplumber
from typing import List, Dict


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
        "企业职工基本养老保险",
        "机关事业养老保险",
    }
    if name in blacklist:
        return False
    return True


def extract_person_records(pdf_path: str) -> List[Dict]:
    """从PDF表格中提取人员记录"""
    records = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 提取当前页的所有表格（可能只有一个）
            tables = page.extract_tables()
            if not tables:
                # 如果没有表格，尝试用文本正则（作为备用）
                text = page.extract_text()
                if text:
                    pattern = re.compile(
                        r"(\d+)\s+(\d{15,18})\s+([\u4e00-\u9fa5]{2,4})"
                    )
                    for match in pattern.finditer(text):
                        seq, id_num, name = match.groups()
                        if is_valid_name(name):
                            records.append(
                                {"序号": int(seq), "证件号码": id_num, "姓名": name}
                            )
                continue

            for table in tables:
                for row in table:
                    if not row or len(row) < 3:
                        continue
                    # 前三个单元格可能包含序号、身份证号、姓名
                    cell0 = str(row[0]).strip() if row[0] else ""
                    cell1 = str(row[1]).strip() if row[1] else ""
                    cell2 = str(row[2]).strip() if row[2] else ""

                    # 尝试识别：第一列为数字序号，第二列为身份证号（15/18位数字），第三列为中文名
                    if (
                        cell0.isdigit()
                        and re.fullmatch(r"\d{15,18}", cell1)
                        and is_valid_name(cell2)
                    ):
                        records.append(
                            {"序号": int(cell0), "证件号码": cell1, "姓名": cell2}
                        )
                    # 有时表格第一列是空，姓名在第二列？但成都格式通常序号在第一列，所以上述优先。
                    # 若上述未匹配，尝试其他组合（例如序号和身份证号可能在同一列？但通常不会）
    # 按序号排序
    records.sort(key=lambda x: x["序号"])
    return records


def main():
    pdf_file = "成都.pdf"  # 根据实际修改
    pdf_file = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\成都.pdf"

    try:
        records = extract_person_records(pdf_file)
        if not records:
            print("未提取到任何有效记录，请检查PDF格式。")
            return

        df = pd.DataFrame(records)
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
