import pdfplumber
import pandas


def parse_social_security_pdf(pdf_path, city_name, file_name, output_excel):
    """
    社保PDF通用解析器
    适配标准参保表格，自动识别表头、姓名列，过滤无效内容、自动去重
    兼容不同pdfplumber版本与表格列偏移问题
    """
    name_set = set()
    # 无效内容过滤词
    filter_words = {"序号", "个人编号", "姓名", "身份证号", "备注", "", " "}
    # 合法表头判定关键字（同时存在则认定为正式表头）
    header_keywords = {"序号", "姓名"}

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue

                header_index = None
                name_col_idx = None

                # 遍历所有行，查找合法表头
                for row_idx, row in enumerate(table):
                    clean_row = [cell.strip() if cell else "" for cell in row]
                    row_word_set = set(clean_row)
                    if header_keywords.issubset(row_word_set):
                        header_index = row_idx
                        # 定位姓名所在列
                        for col_idx, cell in enumerate(clean_row):
                            if cell == "姓名":
                                name_col_idx = col_idx
                                break
                        break

                # 未识别表头/姓名列，跳过当前表格
                if header_index is None or name_col_idx is None:
                    continue

                # 提取表头后的人员数据
                for row in table[header_index + 1 :]:
                    clean_row = [cell.strip() if cell else "" for cell in row]
                    if len(clean_row) <= name_col_idx:
                        continue
                    name = clean_row[name_col_idx]
                    # 姓名规则：非空、非过滤词、常规中文姓名(1-4字符)
                    if name and name not in filter_words and 1 <= len(name) <= 4:
                        name_set.add(name)

    # 组装输出数据
    data_list = []
    for name in name_set:
        data_list.append({"人名": name, "城市名": city_name, "文件名": file_name})
    df = pandas.DataFrame(data_list)
    # 导出Excel，不保留行索引
    df.to_excel(output_excel, index=False, engine="openpyxl")
    return df


# ==================== 配置区域（当前解析昆明）====================
if __name__ == "__main__":
    PDF_PATH = "昆明.pdf"
    PDF_PATH = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\昆明.pdf"
    CITY = "昆明"
    SOURCE_FILE = "昆明.pdf"
    OUTPUT_FILE = "昆明社保人员信息.xlsx"

    result_df = parse_social_security_pdf(PDF_PATH, CITY, SOURCE_FILE, OUTPUT_FILE)

    # 控制台打印结果
    print(f"==== {CITY} 社保参保人员名单 ====")
    print(result_df)

    # 空数据提示
    if result_df.empty:
        print("\n提示：未提取到有效参保人员信息！")
    else:
        print(f"\n解析完成，数据已保存至: {OUTPUT_FILE}")
