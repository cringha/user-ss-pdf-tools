
from parser.hangzhou.parser_name_hangzhou import HangZhouParser

PDF_PATH = r".\data\杭州.pdf"


if __name__ == "__main__":


    result_df = HangZhouParser().parse_file(PDF_PATH)
    # 打印结果
    print("====  社保参保人员名单 ====" ,  len(result_df))

    assert len(result_df) == 11