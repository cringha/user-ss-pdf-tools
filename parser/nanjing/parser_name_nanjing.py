import re
from typing import List

from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser


def extract_social_security_nanjing(pdf_file):
    """
    保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    filter_words = {"单位", "个人"}


    # 1 张译文 32132219840509863X 202501 - 202603 15
    #

    s =   r'^(\d+)\s+([\u4e00-\u9fa5]+)\s+(\d{17}[\dXx])\s+(.*)$'
    pattern = re.compile(s)
    output = []
    items  = common_social_security_extractor(pdf_file, pattern,1)
    for item in items:
        num, name,  id_num,*_ = item
        if name in filter_words:
            print(" name in filter list , ignore ", name)
        else:
            print(f"No{num} - User {name}, id:{id_num}")

            u = SocialSecurityUser(name, id_num)
            output.append(u)


    return output



class NanJingParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        return extract_social_security_nanjing( file_name )
    def get_city_names(self) -> List[str]:
        return ["南京"]


    def snapshot_user(self, file_name: str, user_name: str, target_name: str = None ):
        return self.snapshot_user_base(file_name, user_name, target_name, 10, 10, 5)
