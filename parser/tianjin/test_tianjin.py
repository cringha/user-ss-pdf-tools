from parser.chengdu.parser_name_chengdu import extract_social_security_chengdu
from parser.tianjin.parser_name_tianjin import extract_social_security_tianjin, TianJinParser

PDF_PATH = r".\data\天津.pdf"


def test_chengdu_name_parser():
    result_df = extract_social_security_tianjin(PDF_PATH)
    # 打印结果
    print("==== 保参保人员名单 ====")
    # print(result_df)
    assert len(result_df) == 28


if __name__ == "__main__":

    result_df = TianJinParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 参保人员名单 ====")
    for index, item in enumerate(result_df, start=1):
        print(index, " ", item)

    assert len(result_df) == 28
