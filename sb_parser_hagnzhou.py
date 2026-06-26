import pdfplumber
import pandas


def parse_social_security_pdf(pdf_path, city_name, file_name, output_excel):
    """
    社保PDF通用解析器（适配杭州.pdf）
    规则：
    1. 仅识别包含【序号、姓名】的标准参保表格
    2. 自动定位姓名列，兼容列偏移、库版本差异
    3. 过滤无效内容、自动去重，无人员数据时生成空Excel并提示
    """
    name_set = set()
    # 过滤词汇：表头、空值、无效文本
    filter_words = {
        "序号",
        "姓名",
        "证件号码",
        "身份证号码",
        "实缴时间",
        "参保险种",
        "备注",
        "",
        " ",
    }
    # 合法表头判定关键字
    header_keywords = {"序号", "姓名"}

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue

                header_index = None
                name_col_idx = None

                # 遍历所有行，匹配合法表头
                for row_idx, row in enumerate(table):
                    clean_row = [cell.strip() if cell else "" for cell in row]
                    row_word_set = set(clean_row)
                    if header_keywords.issubset(row_word_set):
                        header_index = row_idx
                        # 定位姓名列
                        for col_idx, cell in enumerate(clean_row):
                            if cell == "姓名":
                                name_col_idx = col_idx
                                break
                        break

                # 无合法表格，跳过
                if header_index is None or name_col_idx is None:
                    continue

                # 提取人员姓名
                for row in table[header_index + 1 :]:
                    clean_row = [cell.strip() if cell else "" for cell in row]
                    if len(clean_row) <= name_col_idx:
                        continue
                    name = clean_row[name_col_idx]
                    # 姓名合法性校验：1-4位常规中文名
                    if name and name not in filter_words and 1 <= len(name) <= 4:
                        name_set.add(name)

    # 组装数据
    data_list = []
    for name in name_set:
        data_list.append({"人名": name, "城市名": city_name, "文件名": file_name})
    df = pandas.DataFrame(data_list)
    # 导出Excel
    df.to_excel(output_excel, index=False, engine="openpyxl")
    return df


# ==================== 配置区 ====================
if __name__ == "__main__":
    # PDF_PATH = "杭州.pdf"
    PDF_PATH = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\杭州.pdf"
    CITY = "杭州"
    SOURCE_FILE = "杭州.pdf"
    OUTPUT_FILE = "杭州社保人员信息.xlsx"

    result_df = parse_social_security_pdf(PDF_PATH, CITY, SOURCE_FILE, OUTPUT_FILE)

    print(f"==== {CITY} 社保参保人员名单 ====")
    print(result_df)

    if result_df.empty:
        print(
            "\n提示：当前PDF文件【未查询到参保人员表格及人员信息】，已生成空Excel文件。"
        )
    else:
        print(f"\n解析完成，数据已保存至: {OUTPUT_FILE}")
