import re
from typing import List

from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser


def extract_social_security_wulumuqi(pdf_file) -> List[SocialSecurityUser]:
    """
    解析福州社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    filter_words = {"单位", "个人"}

    # 序号 证件号码 姓名
    # 202601 202601 1 城职养老 6501100342743 王正仁 在职
    #
    s = r"(\d{6})\s+(\d{6})\s+(\d+)\s+(\w+)\s+(\d+)\s+([\u4e00-\u9fa5]+)\s+([\u4e00-\u9fa5]+)"
    pattern = re.compile(s)
    output = []
    items = common_social_security_extractor(pdf_file, pattern, 5 )
    for item in items:
        _, _, _, _ ,  id_num, name, *_ = item
        if name in filter_words:
            print(" name in filter list , ignore ", name)
        else:
            print(f"  User {name}, id:{id_num}")
            u = SocialSecurityUser(name, id_num)
            output.append(u)

    return output


class WuLuMuQiParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_city_names(self) -> List[str]:
        return ["乌鲁木齐"]

    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        return extract_social_security_wulumuqi(file_name)
