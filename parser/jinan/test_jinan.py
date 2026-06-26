from parser.jinan.parser_name_jinan import JiNanParser


PDF_PATH = r".\data\济南.pdf"


if __name__ == "__main__":


    result_df = JiNanParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 社保参保人员名单 ====", len(result_df)    )

    assert len(result_df) == 29