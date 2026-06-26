from parser.beijing.parser_name_beijing import extract_social_security_beijing


PDF_PATH = r".\data\北京.pdf"
def test_chengdu_name_parser():


    result_df = extract_social_security_beijing(PDF_PATH)
    # 打印结果
    print("==== 福州社保参保人员名单 ====")
    # print(result_df)


if __name__ == "__main__":


    result_df = extract_social_security_beijing(PDF_PATH)
    # 打印结果
    print("==== 福州社保参保人员名单 ====")

    assert len(result_df) == 92