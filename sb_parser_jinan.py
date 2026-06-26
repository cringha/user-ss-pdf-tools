import pdfplumber
import pandas

# 基础配置
PDF_PATH = "济南.pdf"
PDF_PATH = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\济南.pdf"
OUTPUT_EXCEL = "济南社保人员信息.xlsx"
CITY_NAME = "济南"
FILE_NAME = "济南.pdf"


def extract_jinan_social_security(pdf_file):
    """
    解析济南社保PDF，提取参保人员姓名，过滤无效内容并去重
    """
    name_set = set()
    # 定义需要过滤的非人名关键词
    filter_words = {"序号", "身份证号码", "参保险种", "参保起止日期", "备注"}

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            # 提取页面内所有表格
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue
                # 跳过表头，遍历数据行
                for row in table[1:]:
                    # 清洗单元格空格与空值
                    clean_row = [cell.strip() if cell else "" for cell in row]
                    # 表格第二列为姓名
                    name = clean_row[1]
                    # 过滤规则：非空、不在过滤词列表、符合常规姓名长度
                    if name and name not in filter_words and 1 <= len(name) <= 4:
                        name_set.add(name)

    # 组装最终数据
    data = []
    for name in name_set:
        data.append({"人名": name, "城市名": CITY_NAME, "文件名": FILE_NAME})
    df = pandas.DataFrame(data)
    return df


if __name__ == "__main__":
    # 执行解析
    result_df = extract_jinan_social_security(PDF_PATH)
    # 控制台打印结果
    print("==== 济南社保参保人员名单 ====")
    print(result_df)
    # 导出Excel文件
    result_df.to_excel(OUTPUT_EXCEL, index=False, engine="openpyxl")
    print(f"\n解析完成，数据已保存至：{OUTPUT_EXCEL}")
