from parser.chengdu.parser_name_chengdu import extract_social_security_chengdu
from parser.kunming.parser_name_kunming import KunMingParser

PDF_PATH = r".\data\昆明.pdf"
def test__name_parser():

    result_df = extract_social_security_chengdu(PDF_PATH)
    # 打印结果
    print("==== 福州社保参保人员名单 ====")
    # print(result_df)


if __name__ == "__main__":


    result_df = KunMingParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 福州社保参保人员名单 ====")

    assert len(result_df) == 5