import re
from typing import List

from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser


def extract_social_security_guangdong(pdf_file) -> List[SocialSecurityUser]:
    """
     社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    filter_words = {"单位", "个人"}

    # 序号 职工姓名 公民身份号码 基本养老保险 工伤保险 失业保险、
    # 1 蒋辉 341221199208013496

    s = r"(\d+)\s+([\u4e00-\u9fa5]+)\s+([0-9Xx]{18})(.*)"

    pattern = re.compile(s)
    output = []
    items = common_social_security_extractor(pdf_file, pattern, 1)
    num = 0
    for item in items:
        num,  name, id_num,  *_ = item
        if name in filter_words:
            print(" name in filter list , ignore ", name)
        else:
            print(f"No{num} - User {name}, id:{id_num}")
            u = SocialSecurityUser(name, id_num)
            output.append(u)

    return output


from pathlib import Path


def get_last_by_filename_glob(directory, pattern="*"):
    """
    按文件名升序排序，取最后一个
    :param directory: 目录路径
    :param pattern: 通配符模式，如 '*.log', 'report_*'
    """
    dir_path = Path(directory)
    # 获取所有匹配的文件（排除子目录）
    files = [f for f in dir_path.glob(pattern) if f.is_file()]

    if not files:
        print("未找到匹配的文件")
        return None

    # 按文件名（字符串）升序排序，取最后一个
    files_sorted = sorted(files, key=lambda f: f.name)
    return files_sorted[-1]




class GuangDongParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        file = get_last_by_filename_glob( file_name, pattern="*.pdf" )
        if file is None:
            raise FileNotFoundError(file_name)
        return extract_social_security_guangdong(file)
