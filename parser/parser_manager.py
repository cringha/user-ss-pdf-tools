from typing import List

from parser.beijing.parser_name_beijing import BeijingParser
from parser.changchun.parser_name_changchun import ChangChunParser
from parser.changsha.parser_name_changsha import ChangShaParser
from parser.chengdu.parser_name_chengdu import ChengduParser
from parser.chongqing.parser_name_chongqing import ChongQingParser
from parser.common.parser_common import SocialSecurityUser, AbstractParser
from parser.dalian.parser_name_dalian import DaLianParser
from parser.fuzhou.parser_name_fuzhou import FuZhouParser
from parser.guangdong.parser_name_guangdong import GuangDongParser
from parser.hangzhou.parser_name_hangzhou import HangZhouParser
from parser.hefei.parser_name_hefei import HeFeiParser
from parser.jinan.parser_name_jinan import JiNanParser
from parser.kunming.parser_name_kunming import KunMingParser
from parser.nanchang.parser_name_nanchang import NanChangParser
from parser.nanjing.parser_name_nanjing import NanJingParser
from parser.nanning.parser_name_nanning import NanNingParser
from parser.shenyang.parser_name_shenyang import ShenYangParser
from parser.tianjin.parser_name_tianjin import TianJinParser
from parser.wuhan.parser_name_wuhan import WuHanParser
from parser.wulumuqi.parser_name_wulumuqi import WuLuMuQiParser
from parser.yinchuan.parser_name_yinchuan import YinChuanParser
from parser.zhengzhou.parser_name_zhengzhou import ZhengZhouParser

# SS_PARSER_FACTORY = [
#     {"key": "BEI_JING", "name": "北京", "cf": BeijingParser},
#     {"key": "CHANG_CHUN", "name": "长春", "cf": ChangChunParser},
#     {"key": "CHANG_SHA", "name": "长沙", "cf": ChangShaParser},
#     {"key": "CHENG_DU", "name": "成都", "cf": ChengduParser},
#     {"key": "CHONG_QING", "name": "重庆", "cf": ChongQingParser},
#     {"key": "DA_LIAN", "name": "大连", "cf": DaLianParser},
#     {"key": "FU_ZHOU", "name": "福州", "cf": FuZhouParser},
#     {"key": "GUANG_DONG", "name": "广东", "cf": GuangDongParser},
#     {"key": "HANG_ZHOU", "name": "杭州", "cf": HangZhouParser},
#     {"key": "HE_FEI", "name": "合肥", "cf": HeFeiParser},
#     {"key": "JI_NAN", "name": "济南", "cf": JiNanParser},
#     {"key": "KUN_MING", "name": "昆明", "cf": KunMingParser},
#     {"key": "NAN_CHANG", "name": "南昌", "cf": NanChangParser},
#     {"key": "NAN_JING", "name": "南京", "cf": NanJingParser},
#     {"key": "NAN_NING", "name": "南宁", "cf": NanNingParser},
#     {"key": "SHEN_YANG", "name": "沈阳", "cf": ShenYangParser},
#     {"key": "TIAN_JIN", "name": "天津", "cf": TianJinParser},
#     {"key": "WU_HAN", "name": "武汉", "cf": WuHanParser},
#     {"key": "WU_LU_MU_QI", "name": "乌鲁木齐", "cf": WuLuMuQiParser},
#     {"key": "YIN_CHUAN", "name": "银川", "cf": YinChuanParser},
#     {"key": "ZHENG_ZHOU", "name": "郑州", "cf": ZhengZhouParser},
# ]

FACTORYS = [
    BeijingParser,
    ChangChunParser,
    ChangShaParser,
    ChengduParser,
    ChongQingParser,
    DaLianParser,
    FuZhouParser,
    GuangDongParser,
    HangZhouParser,
    HeFeiParser,
    JiNanParser,
    KunMingParser,
    NanChangParser,
    NanJingParser,
    NanNingParser,
    ShenYangParser,
    TianJinParser,
    WuHanParser,
    WuLuMuQiParser,
    YinChuanParser,
    ZhengZhouParser
]
# _KEY_PARSERS = {
#     "BEI_JING": BeijingParser,
#     "CHANG_CHUN": ChangChunParser,
#     "CHANG_SHA": ChangShaParser,
#     "CHENG_DU": ChengduParser,
#     "CHONG_QING": ChongQingParser,
#     "DA_LIAN": DaLianParser,
#     "FU_ZHOU": FuZhouParser,
#     "GUANG_DONG": GuangDongParser,
#     "HANG_ZHOU": HangZhouParser,
#     "HE_FEI": HeFeiParser,
#     "JI_NAN": JiNanParser,
#     "KUN_MING": KunMingParser,
#     "NAN_CHANG": NanChangParser,
#     "NAN_JING": NanJingParser,
#     "NAN_NING": NanNingParser,
#     "SHEN_YANG": ShenYangParser,
#     "TIAN_JIN": TianJinParser,
#     "WU_HAN": WuHanParser,
#     "WU_LU_MU_QI": WuLuMuQiParser,
#     "YIN_CHUAN": YinChuanParser,
#     "ZHENG_ZHOU": ZhengZhouParser,
# }
# _KEY_PARSERS = {}
#
# def _init_key_parsers():
#     for one in SS_PARSER_FACTORY:
#         key = one["key"]
#         name = one["name"]
#         cf = one["cf"]
#         _KEY_PARSERS[key] = cf
#     return _KEY_PARSERS


_CITY_FACTORY_CACHE = {}


def get_city_cf_by_name(city_name):
    if city_name in _CITY_FACTORY_CACHE:
        return _CITY_FACTORY_CACHE[city_name]

    for cf in FACTORYS:
        inst = cf()
        if inst.match_city_name(city_name):
            _CITY_FACTORY_CACHE[city_name] = cf
            return cf

    return None


_FILE_NAME_FACTORY_CACHE = {}


def guess_city_cf_by_filename(file_name: str):
    if file_name in _FILE_NAME_FACTORY_CACHE:
        return _FILE_NAME_FACTORY_CACHE[file_name]
    for cf in FACTORYS:
        inst = cf()
        if inst.match_file_name(file_name):
            _FILE_NAME_FACTORY_CACHE[file_name] = cf
            return cf

    return None


def get_processor_by_city_name(city_name: str, *args, **kwargs) -> AbstractParser | None:
    if city_name is None:
        raise ValueError(f"The city {city_name} empty")

    factory = get_city_cf_by_name(city_name)
    if factory is None:
        return None
    inst = factory(*args, **kwargs)
    return inst


def get_processor_by_file_name(file_name: str, *args, **kwargs) -> AbstractParser | None:
    if file_name is None:
        raise ValueError(f"The file {file_name} empty")

    factory = guess_city_cf_by_filename(file_name)
    if factory is None:
        return None
    inst = factory(*args, **kwargs)
    return inst


def get_processor_by_city(city_name: str, *args, **kwargs):
    return get_processor_by_city_name(city_name, *args, **kwargs)


def parser_ss_file_by_city_name(city_name: str, pdf_file: str, *args, **kwargs) -> List[SocialSecurityUser]:
    inst = get_processor_by_city(city_name, *args, **kwargs)
    if inst is None:
        raise ValueError(f"The {city_name} get inst None")

    return inst.parse_file(pdf_file)


def parser_ss_file_by_file_name(file_name: str, pdf_file: str, *args, **kwargs) -> List[SocialSecurityUser]:
    inst = get_processor_by_file_name(file_name, *args, **kwargs)
    if inst is None:
        raise ValueError(f"The {file_name} get inst None")
    return inst.parse_file(pdf_file)

