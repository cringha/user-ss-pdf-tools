import re
from typing import List


from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser


def extract_social_security_nanchang(pdf_file):
    """
    解析福州社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    filter_words = {"单位", "个人"}


    # 南昌的 表格， 身份证可能不在一行
    # 1 周旺旺 362528199709105511 202506 12 202506 12 202506 12 202506 12
    #

    s =   r'^(\d+)\s+([^\s]+)\s+(?:(\d{17}[\dXx])\s+)?(\d{6})\s+(\d+)\s+(\d{6})\s+(\d+)\s+(\d{6})\s+(\d+)\s+(\d{6})\s+(\d+)$'
    pattern = re.compile(s)
    output = []
    items  = common_social_security_extractor(pdf_file, pattern,1)
    for item in items:
        num, name, id_num,*_ = item
        if name in filter_words:
            print(" name in filter list , ignore ", name)
        else:
            print(f"No{num} - User {name}, id:{id_num}")
            u = SocialSecurityUser(name, id_num)
            output.append(u)

    return output



class NanChangParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_city_names(self) -> List[str]:
        return ["南昌"]

    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        return extract_social_security_nanchang( file_name )


    def snapshot_user(self, file_name: str, user_name: str, target_name: str = None):
        return self.snapshot_user_base(file_name, user_name, target_name,
                                       10, 10, 15, True)
