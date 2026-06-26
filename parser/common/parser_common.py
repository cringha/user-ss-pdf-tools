
import re
from typing import List, Set, Tuple

import pdfplumber


# 基础配置


class SocialSecurityUser:
    def __init__(self, name: str, ss_id: str):
        self.name = name
        self.ss_id = ss_id

    def __str__(self):
        return f'{self.name}, {self.ss_id}'



def to_line( row  ) -> str :
    row_data = [cell.strip().replace("\n", "") if cell else "" for cell in row]
    s = []
    for it in row_data:
        if it is not None and it !="":
            s.append(it)
    return " ".join(s)



def common_extractor_(pdf_file) -> List[str]:
    """
    """
    line_list = []

    # 打开PDF文件
    with pdfplumber.open(pdf_file) as pdf:
        # 逐页读取表格
        for page in pdf.pages:
            # 提取页面内所有表格
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue
                # 遍历表格行，跳过表头
                for row in table :
                    # 去除行内空值、空格
                    # row_data = [cell.strip().replace("\n","") if cell else "" for cell in row]
                    # str_data = " ".join(row_data)
                    # print(" ROW  " , row_data)
                    # print(" ROW- ", str_data)
                    line = to_line(row)
                    if line != "":
                        line_list.append(line)
    return line_list


def common_social_security_extractor(
    pdf_file: str, pattern: re.Pattern, key_index : int
) -> List[Tuple]:
    """
    解析福州社保PDF，提取参保人员姓名，过滤无效内容并去重
    """
    output = []
    lines = common_extractor_( pdf_file )

    exist_keys=set()

    for index, line in enumerate(lines, start=1):
        print(f"行号: {index}, 内容: {line}")
        ll = line.strip()
        match = pattern.match( ll )
        if match:
            groups = match.groups()

            key = groups[key_index]
            if key not in exist_keys:
                exist_keys.add(key)
                output.append(groups)
            else:
                print(f"key_index: {key_index}  key: {key} exist" )
        else:
            print(f" Not match >>>{ll}<<<"   )

        # for match in pattern.finditer(line):
        #     groups = match.groups()
        #
        #     key = groups[key_index]
        #     if key not in exist_keys:
        #         exist_keys.add(key)
        #         output.append(groups)

        # for match in pattern.finditer(line):
        #     groups = match.groups()
        #
        #     key = groups[key_index]
        #     if key not in exist_keys:
        #         exist_keys.add(key)
        #         output.append(groups)
    return output



def common_social_security_extractor_old (
    pdf_file: str, pattern: re.Pattern
) -> List[Tuple]:
    """
    解析福州社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    output = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            # 提取页面所有表格
            print(
                f"Page :{page.page_number}, file :{pdf_file}",
            )

            lines = page.extract_text_lines()
            if not lines:
                continue

            # print("lines ", len(lines))
            for index, line in enumerate(lines, start=1):
                tt = line["text"]

                print(f"行号: {index}, 内容: {tt}")
                for match in pattern.finditer(tt):
                    groups = match.groups()
                    output.append(groups)
                    # seq, id_num, name = match.groups()

        return output


class AbstractParser:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def parse_file(self , file_name:str ) -> List[SocialSecurityUser]:
        pass