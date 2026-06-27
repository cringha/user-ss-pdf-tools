import re
from typing import List

from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser


def extract_social_security_changchun(pdf_file) -> List[SocialSecurityUser]:
    """
     社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    filter_words = {"单位", "个人"}

    # 序号 姓名 身份证号 参工时间
    # 1 曹洋 37012519960615001X 20200901

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


class ChangChunParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def get_city_names(self) -> List[str]:
        return ["长春"]


    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        return extract_social_security_changchun(file_name)
