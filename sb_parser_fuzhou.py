import pdfplumber
import pandas

# 基础配置
PDF_PATH = "福州.pdf"
PDF_PATH = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\福州.pdf"
OUTPUT_EXCEL = "福州社保人员信息.xlsx"
CITY_NAME = "福州"
FILE_NAME = "福州.pdf"


def extract_fuzhou_social_security(pdf_file):
    """
    解析福州社保PDF，提取参保人员姓名，过滤无效内容并去重
    """
    name_set = set()
    # 定义非人名、需要过滤的关键词/无效字符
    filter_words = {"单位", "个人"}

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            # 提取页面所有表格
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue
                # 跳过表头行，遍历数据行
                for row in table[1:]:
                    # 清洗单元格内容
                    clean_row = [cell.strip() if cell else "" for cell in row]
                    # 本表结构：第3列为姓名
                    # print(" cleanrow  ", clean_row)
                    if len(clean_row) < 2:
                        continue
                    name = clean_row[2]
                    # 过滤规则：非空、不在过滤列表、长度符合常规人名
                    if name and name not in filter_words and 1 <= len(name) <= 4:
                        name_set.add(name)

    # 组装结构化数据
    data = []
    for name in name_set:
        data.append({"人名": name, "城市名": CITY_NAME, "文件名": FILE_NAME})
    df = pandas.DataFrame(data)
    return df


if __name__ == "__main__":
    result_df = extract_fuzhou_social_security(PDF_PATH)
    # 打印结果
    print("==== 福州社保参保人员名单 ====")
    print(result_df)
    # 导出Excel
    result_df.to_excel(OUTPUT_EXCEL, index=False, engine="openpyxl")
    print(f"\n解析完成，数据已保存至 {OUTPUT_EXCEL}")
