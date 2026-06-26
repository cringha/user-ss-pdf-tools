import pdfplumber
import pandas

# 基础配置
# PDF_PATH = "长春.pdf"       # PDF文件路径
PDF_PATH = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\长春.pdf"
OUTPUT_EXCEL = "长春社保人员信息.xlsx"  # 输出Excel路径
CITY = "长春"  # 对应城市
FILE_NAME = "长春.pdf"  # 源文件名


def extract_changsha_pdf(pdf_file):
    """
    解析长春社保PDF表格，提取参保人员信息
    :param pdf_file: PDF文件路径
    :return: 结构化DataFrame
    """
    person_list = []

    # 打开PDF文件
    with pdfplumber.open(pdf_file) as pdf:
        # 逐页读取表格
        for page in pdf.pages:
            # 提取页面内所有表格
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue
                # 遍历表格行，跳过表头
                for row in table[1:]:
                    # 去除行内空值、空格
                    row_data = [cell.strip() if cell else "" for cell in row]
                    # 第二列为姓名（对应表格：序号 | 姓名 | 身份证号 ...）
                    name = row_data[1]
                    if name:  # 过滤空姓名
                        person_list.append(
                            {"人名": name, "城市名": CITY, "文件名": FILE_NAME}
                        )

    # 转为DataFrame
    df = pandas.DataFrame(person_list)
    return df


if __name__ == "__main__":
    # 执行解析
    result_df = extract_changsha_pdf(PDF_PATH)

    # 控制台打印结果
    print("==== 长春社保参保人员信息 ====")
    print(result_df)

    # 导出Excel（不保留行索引）
    result_df.to_excel(OUTPUT_EXCEL, index=False, engine="openpyxl")
    print(f"\n解析完成！数据已保存至：{OUTPUT_EXCEL}")
