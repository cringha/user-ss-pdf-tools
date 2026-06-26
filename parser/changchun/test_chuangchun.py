from parser.changchun.parser_name_changchun import ChangChunParser

PDF_PATH = r".\data\长春.pdf"

if __name__ == "__main__":
    result_df = ChangChunParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 社保参保人员名单 ====", len(result_df))

    assert len(result_df) == 7
