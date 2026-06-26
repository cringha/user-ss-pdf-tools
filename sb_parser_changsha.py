import pdfplumber
import pandas

# ===================== 配置区域 =====================
# PDF文件路径（修改为你的实际文件路径）
pdf_path = r"C:\Users\101202304023\Desktop\工作\投标项目\社保-20260603\长沙.pdf"
# 输出Excel文件路径
excel_out_path = "长沙社保人员信息.xlsx"
# 固定城市与文件名
city_name = "长沙"
file_name = "长沙.pdf"
# ====================================================


def extract_changsha_social_security(pdf_file):
    """
    解析长沙社保证明PDF，提取参保人员姓名
    :param pdf_file: PDF文件路径
    :return: 结构化DataFrame
    """
    name_list = []
    # 打开PDF
    with pdfplumber.open(pdf_file) as pdf:
        # 遍历PDF所有页面
        for page in pdf.pages:
            # 提取页面纯文本
            page_text = page.extract_text()
            if not page_text:
                continue
            # 按行分割文本
            lines = page_text.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # 匹配身份证+姓名格式（长沙表格核心行特征）
                # 规则：行首为18位身份证号，后跟姓名
                if len(line) >= 20 and line[0].isdigit():
                    # 分割字段（按空格拆分）
                    parts = line.split()
                    # 过滤：第一个元素是身份证，第二个为姓名
                    if len(parts) >= 2 and len(parts[0]) in (18, 17):
                        person_name = parts[1]
                        # 去重添加
                        if person_name not in name_list:
                            name_list.append(person_name)

    # 构造DataFrame：姓名、城市、文件名
    data = []
    for name in name_list:
        data.append({"人名": name, "城市名": city_name, "文件名": file_name})
    df = pandas.DataFrame(data)
    return df


if __name__ == "__main__":
    # 执行解析
    result_df = extract_changsha_social_security(pdf_path)
    # 控制台打印结果
    print("===== 长沙社保参保人员信息 =====")
    print(result_df)
    # 导出为Excel
    result_df.to_excel(excel_out_path, index=False, engine="openpyxl")
    print(f"\n解析完成！数据已导出至：{excel_out_path}")
