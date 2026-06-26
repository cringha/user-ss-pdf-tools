
from parser.wuhan.parser_name_wuhan import WuHanParser

PDF_PATH = r".\data\武汉.pdf"


if __name__ == "__main__":


    result_df = WuHanParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 社保参保人员名单 ====", len(result_df)    )

    assert len(result_df) == 42