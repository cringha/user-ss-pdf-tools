from parser.chengdu.parser_name_chengdu import extract_social_security_chengdu
from parser.wulumuqi.parser_name_wulumuqi import WuLuMuQiParser

PDF_PATH = r".\data\乌鲁木齐.pdf"


def test_chengdu_name_parser():
    result_df = extract_social_security_chengdu(PDF_PATH)
    # 打印结果
    print("==== 乌鲁木齐社保参保人员名单 ====")
    # print(result_df)


if __name__ == "__main__":
    result_df = WuLuMuQiParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 乌鲁木齐社保参保人员名单 ====")

    assert len(result_df) == 16
