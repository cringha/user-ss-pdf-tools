from parser.fuzhou.parser_name_fuzhou import FuZhouParser


PDF_PATH = r".\data\福州.pdf"


if __name__ == "__main__":


    result_df = FuZhouParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 社保参保人员名单 ====", len(result_df)    )

    assert len(result_df) == 24