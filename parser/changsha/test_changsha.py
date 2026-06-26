from parser.changsha.parser_name_changsha import ChangShaParser

PDF_PATH = r".\data\长沙.pdf"

if __name__ == "__main__":
    result_df = ChangShaParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 社保参保人员名单 ====", len(result_df))

    assert len(result_df) == 14
