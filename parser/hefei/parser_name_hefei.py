import re
from typing import List

from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser


def extract_social_security_hefei(pdf_file):
    """
    解析福州社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    filter_words = {"单位", "个人"}

    # 序号 姓名 社会保障号码 险种 参保情况 本单位实际缴费月数
    # '3 汪学群 120225198411296056 失业保险 202505 202605 13'
    #

    s = r'^(\d+)\s+([\u4e00-\u9fa5]+)\s+(\d{17}[\dXx])\s+(\d+)\s+(\d+)\s+(\d+)$'
    pattern = re.compile(s)
    output = []
    items = common_social_security_extractor(pdf_file, pattern, 1)
    for item in items:
        num, name, id_num, *_ = item
        if name in filter_words:
            print(" name in filter list , ignore ", name)
        else:
            print(f"No{num} - User {name}, id:{id_num}")
            u = SocialSecurityUser(name, id_num)
            output.append(u)

    return output


class HeFeiParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        return extract_social_security_hefei(file_name)
