import re
from typing import List

from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser


def extract_social_security_beijing(pdf_file)-> List[SocialSecurityUser]:
    """
    解析福州社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    filter_words = {"单位", "个人"}

    #  序号 姓名 社会保障号码 险种
    #  1 刘晨 420621198912015117
    #
    s = r'^(\d+)\s+([\u4e00-\u9fa5]+)\s+(\d{17}[\dXx])(.*)$'

    pattern = re.compile(s)
    output = []
    items = common_social_security_extractor(pdf_file, pattern, 2)
    for item in items:
        num, name,  id_num, *_ = item
        if name in filter_words:
            print(" name in filter list , ignore ", name)
        else:
            print(f"No{num} - User {name}, id:{id_num}")
            u = SocialSecurityUser(name, id_num)
            output.append(u)

    return output


class BeijingParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        return extract_social_security_beijing( file_name )