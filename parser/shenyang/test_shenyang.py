from parser.shenyang.parser_name_shenyang import ShenYangParser

PDF_PATH = r".\data\沈阳.pdf"


if __name__ == "__main__":


    result_df = ShenYangParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 社保参保人员名单 ====", len(result_df)    )

    assert len(result_df) == 20