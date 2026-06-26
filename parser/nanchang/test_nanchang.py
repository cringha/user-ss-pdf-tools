import pdfplumber

from parser.nanchang.parser_name_nanchang import extract_social_security_nanchang, NanChangParser

PDF_PATH = r".\data\南昌.pdf"
def test_chengdu_name_parser():


    result_df = extract_social_security_nanchang(PDF_PATH)
    # 打印结果
    print("==== 保参保人员名单 ====")
    # print(result_df)
    assert len(result_df) == 11



if __name__ == "__main__":

    result_df = NanChangParser().parse_file(PDF_PATH)
    # result_df = extract_social_security_nanchang(PDF_PATH)
    # 打印结果
    # print("==== 参保人员名单 ====")
    # print(result_df)
    assert len(result_df) == 7