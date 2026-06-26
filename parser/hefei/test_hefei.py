from parser.hefei.parser_name_hefei import extract_social_security_hefei, HeFeiParser

PDF_PATH = r".\data\合肥.pdf"


def test_chengdu_name_parser():
    result_df = extract_social_security_hefei(PDF_PATH)
    # 打印结果
    print("==== 保参保人员名单 ====")
    # print(result_df)
    assert len(result_df) == 11


if __name__ == "__main__":
    result_df = HeFeiParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 参保人员名单 ====")
    # print(result_df)
    assert len(result_df) == 4
