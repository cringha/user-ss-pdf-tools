from parser.nanning.parser_name_nanning import extract_social_security_nanning, NanNingParser

PDF_PATH = r".\data\南宁.pdf"


def test_chengdu_name_parser():
    result_df = NanNingParser().parse_file(PDF_PATH)
    # 打印结果extract_social_security_nanning
    print("==== 保参保人员名单 ====")
    # print(result_df)
    assert len(result_df) == 11


if __name__ == "__main__":

    result_df = NanNingParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 参保人员名单 ====")
    # print(result_df)

    for index, item in enumerate(result_df, start=1):
        print(index, " ", item)

    assert len(result_df) == 10
