import re
from typing import List

from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser


def extract_social_security_yinchuan(pdf_file) -> List[SocialSecurityUser]:
    """
     社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    filter_words = {"单位", "个人"}

    # 个人编号 姓名 证件号码 险种类型 所属期 缴费期 缴费基数 单位缴纳 个人缴纳 缴费标志 到账时间
    # 1000970554 蔡骏潇 640102199008051514 职工养老保险 202505 202505 已到账 20250523

    s = r"(\d+)\s+([\u4e00-\u9fa5]+)\s+([0-9Xx]{18})(.*)"

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


class YinChuanParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        return extract_social_security_yinchuan(file_name)
