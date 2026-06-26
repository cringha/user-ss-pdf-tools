#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import pandas as pd
import pdfplumber


def is_valid_name(name: str) -> bool:
    """判断字符串是否为合理的中文人名（2~4个汉字，不含特殊字符）"""
    if not isinstance(name, str):
        return False
    name = name.strip()
    # 必须全是中文且长度在2~4之间
    if not re.fullmatch(r"[\u4e00-\u9fa5]{2,4}", name):
        return False
    # 排除常见的非人名关键词
    blacklist = {
        "序号",
        "姓名",
        "身份证号",
        "个人编号",
        "缴费起止时间",
        "缴费状态",
        "年/月",
        "单位名称",
        "单位编号",
        "备注",
        "验证平台",
        "授权码",
        "社会保障号",
        "实缴到账",
        "做账期号",
        "参保所属地",
    }
    if name in blacklist:
        return False
    return True


def extract_names_from_pdf(pdf_path: str) -> list:
    """
    从PDF中提取所有有效人名的列表（保持出现顺序，去重保留首次出现）
    """
    # 正则：行首可能有空格，然后是序号（数字）、姓名（中文2-4字）、身份证号（15或18位）
    # 示例："1 彭文凯 420115199202148337 10048880229 ..."
    pattern = re.compile(
        r"^\s*(\d+)\s+"  # 序号
        r"([\u4e00-\u9fa5]{2,4})\s+"  # 姓名
        r"(\d{15,18})"  # 身份证号
    )

    names = []
    seen = set()

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                match = pattern.match(line)
                if match:
                    seq, name, id_num = match.groups()
                    if is_valid_name(name) and name not in seen:
                        seen.add(name)
                        names.append(name)
                else:
                    # 某些行可能因为换行导致姓名和身份证号被拆分，但当前PDF格式规整，无需额外处理
                    pass

    if not names:
        raise ValueError("未从PDF中提取到任何有效人名，请检查PDF格式或文件路径。")

    return names


PDF_PATH = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\武汉.pdf"


def main():
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
    else:
        pdf_file = PDF_PATH  # 根据实际文件名修改

    try:
        names = extract_names_from_pdf(pdf_file)
        # 构造DataFrame：姓名 + 固定城市“武汉”
        df = pd.DataFrame({"姓名": names, "城市": ["武汉"] * len(names)})

        print(f"成功提取 {len(names)} 条人员信息：")
        print(df.to_string(index=False))

        # 保存为CSV
        output_csv = "武汉_社保人员.csv"
        df.to_csv(output_csv, index=False, encoding="utf-8-sig")
        print(f"\n数据已保存至：{output_csv}")

    except Exception as e:
        print(f"错误：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
