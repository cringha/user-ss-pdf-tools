
from parser.guangdong.parser_name_guangdong import GuangDongParser

PDF_PATH = r".\data\广州一个月一张"

if __name__ == "__main__":
    result_df = GuangDongParser().parse_file(PDF_PATH)
    # 打印结果
    print("==== 社保参保人员名单 ====", len(result_df))
    assert len(result_df) == 43
