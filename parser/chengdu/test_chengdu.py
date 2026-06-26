from parser.chengdu.parser_name_chengdu import extract_social_security_chengdu, ChengduParser


def test_chengdu_name_parser():
    PDF_PATH = r".\data\成都.pdf"

    result_df = extract_social_security_chengdu(PDF_PATH)
    # 打印结果
    print("==== 福州社保参保人员名单 ====")
    # print(result_df)


if __name__ == "__main__":
    PDF_PATH = r".\data\成都.pdf"

    result_df = ChengduParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 福州社保参保人员名单 ====")

    assert len(result_df) == 20