#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import pandas as pd
import pdfplumber
import sys


def is_valid_name(name: str) -> bool:
    """
    判断字符串是否是一个合理的人名。
    规则：
    - 只包含中文字符（至少两个，最多四个）
    - 不包含常见的非人名关键词（如“序号”、“姓名”等）
    """
    if not isinstance(name, str):
        return False
    name = name.strip()
    # 检查是否全部为中文且长度在2~4之间
    if not re.fullmatch(r"[\u4e00-\u9fa5]{2,4}", name):
        return False
    # 过滤掉表头或提示性文字
    blacklist = {"序号", "姓名", "证件号码", "实缴时间", "缴费人员名单", "单位登记证号"}
    if name in blacklist:
        return False
    return True


def parse_pdf_to_dataframe(pdf_path: str) -> pd.DataFrame:
    """
    从PDF中提取社保缴费人员信息，返回DataFrame。
    期望的表格格式：序号、姓名、证件号码、实缴时间（如“202210-202605”）
    """
    records = []
    # 正则匹配一行有效数据：序号 姓名 身份证号 起始-结束月份
    # 身份证号可能是15位或18位，日期段格式为YYYYMM-YYYYMM
    pattern = re.compile(
        r"^(\d+)\s+"  # 序号
        r"([\u4e00-\u9fa5]{2,4})\s+"  # 姓名（中文2-4字）
        r"(\d{15,18})\s+"  # 证件号码
        r"(\d{6}-\d{6})$"  # 实缴时间区间
    )

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 提取整页文本
            text = page.extract_text()
            if not text:
                continue
            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                match = pattern.match(line)
                if match:
                    seq, name, id_num, period = match.groups()
                    # 进一步过滤不合理的人名（例如“单位登记证号”等不会被正则匹配到，但以防万一）
                    if is_valid_name(name):
                        records.append(
                            {
                                "序号": int(seq),
                                "姓名": name,
                                "证件号码": id_num,
                                "实缴时间": period,
                            }
                        )
                else:
                    # 如果整行不匹配，但可能因为空格数量不固定导致部分行被拆分？本例中PDF格式规整，无需额外处理
                    pass

    if not records:
        raise ValueError("未从PDF中提取到任何有效的人员数据，请检查PDF格式或文件路径。")

    df = pd.DataFrame(records)
    return df


# 基础配置
PDF_PATH = "沈阳.pdf"
PDF_PATH = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\沈阳.pdf"


def main():
    # 默认PDF文件名，也可通过命令行参数传入
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
    else:
        pdf_file = PDF_PATH

    try:
        df = parse_pdf_to_dataframe(pdf_file)
        print(f"成功提取 {len(df)} 条人员信息：")
        print(df.to_string(index=False))

        # 保存为CSV文件
        output_csv = "社保人员信息.csv"
        df.to_csv(output_csv, index=False, encoding="utf-8-sig")
        print(f"\n数据已保存至：{output_csv}")

        # 可选：同时保存为Excel（需要安装openpyxl）
        # df.to_excel("社保人员信息.xlsx", index=False)

    except Exception as e:
        print(f"错误：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
