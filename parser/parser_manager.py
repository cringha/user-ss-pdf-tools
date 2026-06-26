from typing import List

from parser.beijing.parser_name_beijing import BeijingParser
from parser.changchun.parser_name_changchun import ChangChunParser
from parser.changsha.parser_name_changsha import ChangShaParser
from parser.chengdu.parser_name_chengdu import ChengduParser
from parser.chongqing.parser_name_chongqing import ChongQingParser
from parser.common.parser_common import SocialSecurityUser
from parser.dalian.parser_name_dalian import DaLianParser
from parser.fuzhou.parser_name_fuzhou import FuZhouParser
from parser.guangdong.parser_name_guangdong import GuangDongParser
from parser.hangzhou.parser_name_hangzhou import HangZhouParser
from parser.hefei.parser_name_hefei import HeFeiParser
from parser.jinan.parser_name_jinan import JiNanParser
from parser.kunming.parser_name_kunming import KunMingParser
from parser.nanchang.parser_name_nanchang import NanChangParser
from parser.nanjing.parser_name_nanjing import NanJingParser
from parser.shenyang.parser_name_shenyang import ShenYangParser
from parser.tianjin.parser_name_tianjin import TianJinParser
from parser.wuhan.parser_name_wuhan import WuHanParser
from parser.wulumuqi.parser_name_wulumuqi import WuLuMuQiParser
from parser.yinchuan.parser_name_yinchuan import YinChuanParser
from parser.zhengzhou.parser_name_zhengzhou import ZhengZhouParser

SS_PARSER_FACTORY = [
    {"key": "BEI_JING", "name": "北京", "cf": BeijingParser},
    {"key": "CHANG_CHUN", "name": "长春", "cf": ChangChunParser},
    {"key": "CHANG_SHA", "name": "长沙", "cf": ChangShaParser},
    {"key": "CHENG_DU", "name": "成都", "cf": ChengduParser},
    {"key": "CHONG_QING", "name": "重庆", "cf": ChongQingParser},
    {"key": "DA_LIAN", "name": "大连", "cf": DaLianParser},
    {"key": "FU_ZHOU", "name": "福州", "cf": FuZhouParser},
    {"key": "GUANG_DONG", "name": "广东", "cf": GuangDongParser},
    {"key": "HANG_ZHOU", "name": "杭州", "cf": HangZhouParser},
    {"key": "HE_FEI", "name": "合肥", "cf": HeFeiParser},
    {"key": "JI_NAN", "name": "济南", "cf": JiNanParser},
    {"key": "KUN_MING", "name": "昆明", "cf": KunMingParser},
    {"key": "NAN_CHANG", "name": "南昌", "cf": NanChangParser},
    {"key": "NAN_JING", "name": "南京", "cf": NanJingParser},
    {"key": "NAN_NING", "name": "南宁", "cf": NanJingParser},
    {"key": "SHEN_YANG", "name": "沈阳", "cf": ShenYangParser},
    {"key": "TIAN_JIN", "name": "天津", "cf": TianJinParser},
    {"key": "WU_HAN", "name": "武汉", "cf": WuHanParser},
    {"key": "WU_LU_MU_QI", "name": "乌鲁木齐", "cf": WuLuMuQiParser},
    {"key": "YIN_CHUAN", "name": "银川", "cf": YinChuanParser},
    {"key": "ZHENG_ZHOU", "name": "郑州", "cf": ZhengZhouParser},
]


_KEY_PARSERS = {}

def _init_key_parsers():
    for one in SS_PARSER_FACTORY:
        key = one["key"]
        name = one["name"]
        cf = one["cf"]
        _KEY_PARSERS[key] = cf
    return _KEY_PARSERS

def get_city_key_by_name(city_name):
    for one in SS_PARSER_FACTORY:
        key = one["key"]
        name = one["name"]
        if city_name == name:
            return key
    return None

def parser_ss_file(city_key: str, pdf_file: str, *args, **kwargs) -> List[SocialSecurityUser]:

    if len(_KEY_PARSERS) == 0:
        _init_key_parsers()

    if city_key not in _KEY_PARSERS:
        raise ValueError(f"The city {city_key} does not exist")
    factory = _KEY_PARSERS[city_key]
    inst = factory(args, kwargs)
    return inst.parse_file(pdf_file)




if __name__ == "__main__":
    PDF_PATH = r".\data\成都.pdf"

    result_df = parser_ss_file("CHENG_DU", PDF_PATH)
    # 打印结果
    print("==== 福州社保参保人员名单 ====")

    assert len(result_df) == 20
