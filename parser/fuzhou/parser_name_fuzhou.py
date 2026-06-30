import re
from typing import List

from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser


def extract_social_security_fuzhou(pdf_file)-> List[SocialSecurityUser]:
    """
    解析福州社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    filter_words = {"单位", "个人"}


    #
    s =  r"(\d+)\s+([0-9Xx]{18})\s+([\u4e00-\u9fa5]+)\s+(\d+)(.*)"

    pattern = re.compile(s)
    output = []
    items = common_social_security_extractor(pdf_file, pattern, 2)
    for item in items:
        num, id_num, name,  *_ = item
        if name in filter_words:
            print(" name in filter list , ignore ", name)
        else:
            print(f"No{num} - User {name}, id:{id_num}")
            u = SocialSecurityUser(name, id_num)
            output.append(u)

    return output


class FuZhouParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_city_names(self) -> List[str]:
        return ["福州"]

    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        return extract_social_security_fuzhou( file_name )

    def snapshot_user(self, file_name: str, user_name: str, target_name: str = None):
        return self.snapshot_user_base(file_name, user_name, target_name, 10, 10, 5, False)
