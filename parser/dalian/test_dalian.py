from parser.chengdu.parser_name_chengdu import extract_social_security_chengdu
from parser.dalian.parser_name_dalian import extract_social_security_dalian, DaLianParser

PDF_PATH = r".\data\大连.pdf"
def test_chengdu_name_parser():

    result_df = extract_social_security_dalian(PDF_PATH)
    # 打印结果
    print("==== 保参保人员名单 ====")
    # print(result_df)
    assert len(result_df) == 11


if __name__ == "__main__":


    result_df = DaLianParser().parse_file (PDF_PATH)
    # 打印结果
    assert len(result_df) == 11