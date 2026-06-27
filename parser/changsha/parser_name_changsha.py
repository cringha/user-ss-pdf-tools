import re
from typing import List

from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser


def extract_social_security_changsha(pdf_file) -> List[SocialSecurityUser]:
    """
     社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    filter_words = {"单位", "个人"}

    # 身份证号码 姓名 性别 当前参保状态
    # 430124198711264276 刘畅 男 正常参保

    s = r"([0-9Xx]{18})\s+([\u4e00-\u9fa5]+)\s+(.*)"

    pattern = re.compile(s)
    output = []
    items = common_social_security_extractor(pdf_file, pattern, 1)
    num = 0
    for item in items:
        id_num, name,  *_ = item
        if name in filter_words:
            print(" name in filter list , ignore ", name)
        else:
            print(f"No{num} - User {name}, id:{id_num}")
            u = SocialSecurityUser(name, id_num)
            output.append(u)
        num+= 1
    return output


class ChangShaParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_city_names(self) -> List[str]:
        return ["长沙"]


    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        return extract_social_security_changsha(file_name)
