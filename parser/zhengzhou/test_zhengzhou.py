from parser.zhengzhou.parser_name_zhengzhou import ZhengZhouParser

PDF_PATH = r".\data\郑州.pdf"

if __name__ == "__main__":
    result_df = ZhengZhouParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 社保参保人员名单 ====", len(result_df))

    assert len(result_df) == 11
