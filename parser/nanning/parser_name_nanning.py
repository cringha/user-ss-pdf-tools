import re
from typing import List

from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser


def extract_social_security_nanning(pdf_file):
    """
    解析福州社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    filter_words = {"单位", "个人"}

    # 14 朱坤宇 451145569403 450924199912176856 失业保险 202505-202605
    #

    s = r'^(\d+)\s+([^\s]+)\s+(\d+)\s+(\d+)\s+([^\s]+)\s+(\d{6}-\d{6})$'
    pattern = re.compile(s)
    output = []
    items = common_social_security_extractor(pdf_file, pattern, 1)
    for item in items:
        num, name, _, id_num, *_ = item
        if name in filter_words:
            print(" name in filter list , ignore ", name)
        else:
            print(f"No{num} - User {name}, id:{id_num}")

            u = SocialSecurityUser(name, id_num)
            output.append(u)

    return output


class NanNingParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        return extract_social_security_nanning(file_name)
