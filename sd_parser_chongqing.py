import pdfplumber
import pandas

# 基础配置
# PDF_FILE = "重庆.pdf"  # PDF文件路径
PDF_FILE = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\重庆.pdf"
OUTPUT_EXCEL = "重庆社保人员信息.xlsx"  # 输出Excel路径
CITY_NAME = "重庆"  # 对应城市
SOURCE_FILE = "重庆.pdf"  # 源文件名


def extract_chongqing_social_security(pdf_path):
    """
    解析重庆社保PDF，提取参保人员姓名并去重
    """
    name_set = set()  # 使用集合自动去重

    with pdfplumber.open(pdf_path) as pdf:
        # 遍历所有页面
        for page in pdf.pages:
            # 提取页面内所有表格
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue
                # 跳过表头行，遍历数据行
                for row in table[1:]:
                    # 清洗单元格空值与空格
                    clean_row = [cell.strip() if cell else "" for cell in row]
                    # 表格第3列为【姓名】
                    name = clean_row[2]
                    if name:
                        name_set.add(name)

    # 转为列表并构造DataFrame
    data_list = []
    for name in name_set:
        data_list.append({"人名": name, "城市名": CITY_NAME, "文件名": SOURCE_FILE})
    df = pandas.DataFrame(data_list)
    return df


if __name__ == "__main__":
    # 执行解析
    result_df = extract_chongqing_social_security(PDF_FILE)

    # 控制台打印结果
    print("==== 重庆社保参保人员名单 ====")
    print(result_df)

    # 导出Excel，不生成行索引
    result_df.to_excel(OUTPUT_EXCEL, index=False, engine="openpyxl")
    print(f"\n解析完成，数据已保存至：{OUTPUT_EXCEL}")
