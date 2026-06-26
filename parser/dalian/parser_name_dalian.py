import re
from typing import List

from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser


def extract_social_security_dalian(pdf_file):
    filter_words = {"单位", "个人"}

    # 序号 姓名 社会保障号码 险种 参保情况 本单位实际缴费月数
    # '3 汪学群 120225198411296056 失业保险 202505 202605 13'
    #

    s = r'^(\d+)\s+([^\s]+)\s+(\d{17}[\dXx])\s+(\d{6})-(\d{6})$'
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


class DaLianParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        return extract_social_security_dalian(file_name)
