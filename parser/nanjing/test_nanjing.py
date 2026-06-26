from parser.nanjing.parser_name_nanjing import extract_social_security_nanjing, NanJingParser


def test_chengdu_name_parser():
    PDF_PATH = r".\data\大连.pdf"

    result_df = extract_social_security_nanjing(PDF_PATH)
    # 打印结果extract_social_security_nanning
    print("==== 保参保人员名单 ====")
    # print(result_df)
    assert len(result_df) == 11


if __name__ == "__main__":
    PDF_PATH = r".\data\南京.pdf"

    result_df = NanJingParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 参保人员名单 ====")
    # print(result_df)

    for index, item in enumerate(result_df, start=1):
        print( index, " ",  item )

    assert len(result_df) == 45