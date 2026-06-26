from parser.chongqing.parser_name_chongqing import ChongQingParser

PDF_PATH = r".\data\重庆.pdf"

if __name__ == "__main__":
    result_df = ChongQingParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 社保参保人员名单 ====", len(result_df))

    assert len(result_df) == 18
