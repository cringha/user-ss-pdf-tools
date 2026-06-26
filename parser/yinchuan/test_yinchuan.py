
from parser.yinchuan.parser_name_yinchuan import YinChuanParser

PDF_PATH = r".\data\银川.pdf"

if __name__ == "__main__":
    result_df = YinChuanParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 社保参保人员名单 ====", len(result_df))

    assert len(result_df) == 4
