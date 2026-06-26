import pdfplumber
import pandas

# 基础配置
PDF_FILE = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\郑州.pdf"
OUTPUT_EXCEL = "郑州社保人员信息.xlsx"  # 输出 Excel 路径
CITY = "郑州"  # 对应城市
FILE_NAME = "郑州.pdf"  # 源文件名

SKIP_NAMES = ["姓名"]


def extract_zhengzhou_pdf(pdf_file):
    """解析郑州社保PDF，提取有效参保姓名"""
    name_list = []

    with pdfplumber.open(pdf_file) as pdf:
        # 遍历所有页面
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue
                # 跳过表头，遍历数据行
                for row in table[1:]:
                    # 清洗单元格空格与空值
                    clean_row = [
                        cell.strip() if cell and cell.strip() else "" for cell in row
                    ]
                    # 表格第二列为姓名
                    name = clean_row[1]
                    # 过滤空姓名、无效内容
                    if name and name not in SKIP_NAMES:
                        name_list.append(name)

    # 去重并构造结构化数据
    unique_names = list(set(name_list))
    data = []
    for name in unique_names:
        data.append({"人名": name, "城市名": CITY, "文件名": FILE_NAME})

    df = pandas.DataFrame(data)
    return df


if __name__ == "__main__":
    # 执行解析
    result_df = extract_zhengzhou_pdf(PDF_FILE)

    # 控制台打印结果
    print("==== 郑州社保参保人员名单 ====")
    print(result_df)

    # 导出 Excel（不保留行索引）
    result_df.to_excel(OUTPUT_EXCEL, index=False, engine="openpyxl")
    print(f"\n解析完成！文件已保存至：{OUTPUT_EXCEL}")
