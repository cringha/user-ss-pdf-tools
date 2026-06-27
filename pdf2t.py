from pathlib import Path
import os
import pandas as pd

import fitz  # PyMuPDF，用于PDF处理

BORDER_WIDTH = 4


def snapshot(doc, page_num, output_dir, filename):
    # 2. 截取首页（第一个包含目标人员的页面）
    first_page = doc[page_num]
    # 将页面转为图片（分辨率300dpi，保证清晰度）
    mat = fitz.Matrix(300 / 72, 300 / 72)
    first_pix = first_page.get_pixmap(matrix=mat)
    png_name = f"{filename}.png"
    first_pix.save(os.path.join(output_dir, png_name))
    print(f"截图已保存：{png_name}")


"""

"""


def process_social_security_pdf_base(
        pdf_path,
        target_name,
        output_dir="screenshots",
        left_offset=10,
        right_offset=10,
        height_offset=20,
        first_and_last_page=True,
        output_prefix="",
        fn_process=None,
):
    """
    处理社保PDF文件，定位指定人员并截图（首页/尾页），人员信息加红框

    Args:
        :param first_and_last_page: 是否要截取首页及尾页
        :param pdf_path:  PDF文件路径
        :param target_name: 要定位的人员姓名
        :param height_offset: 狂徒的高度
        :param right_offset: 画框框的右边的 offset 像素位置，一般是整个页面宽度
        :param output_dir:  截图保存目录
        :param left_offset: 画框框的左边的 offset 像素位置
    """

    # 打开PDF文件
    doc = fitz.open(pdf_path)
    if doc.page_count == 0:
        print("PDF文件为空，无法处理, {pdf_path}")
        return

    # 存储包含目标人员的页面编号
    target_pages = []
    rect_list = []  # 存储目标人员位置的矩形框

    # 1. 遍历PDF页面，查找目标人员并添加红色框
    for page_num in range(doc.page_count):
        page = doc[page_num]

        if fn_process is not None:
            fn_process(page)

        # 搜索目标姓名（支持模糊匹配，可根据实际调整）
        text_instances = page.search_for(target_name)
        page_rect = page.rect
        page_width = page_rect.width

        if text_instances:
            target_pages.append(page_num)
            # 给找到的文本添加红色框
            for rect in text_instances:
                # 调整矩形框大小，让框更美观（上下左右各扩展2个单位）
                # rect = fitz.Rect(rect.x0-X0_OFFSET, rect.y0-Y0_OFFSET,
                #                   page_rect.x1+X1_OFFSET, rect.y1+Y1_OFFSET)
                rect = fitz.Rect(
                    left_offset,
                    rect.y0 - height_offset,
                    page_rect.width - right_offset,
                    rect.y1 + height_offset,
                )
                rect_list.append(rect)
                # 添加红色框：width是框线宽度，color是RGB红色
                annot = page.add_rect_annot(rect)
                # annot = page.last_annot
                annot.set_colors(stroke=(1, 0, 0))  # 边框红色
                annot.set_border(width=BORDER_WIDTH)  # 边框宽度2px
                annot.update()

    # 检查是否找到目标人员``
    if not target_pages:
        print(f"未在PDF中找到人员：{target_name}, {pdf_path}")
        return

        # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    total_count = doc.page_count
    if total_count == 1:  # 就一页，直接截图
        snapshot(doc, 0, output_dir, f"{target_name}_{output_prefix}_00")
    else:
        if len(target_pages) == 1:
            first_page_num = target_pages[0]

            if first_and_last_page:
                snapshot(doc, 0, output_dir, f"{target_name}_{output_prefix}_00")

            if first_and_last_page:
                if first_page_num != 0 and first_page_num != total_count - 1:
                    snapshot(
                        doc,
                        first_page_num,
                        output_dir,
                        f"{target_name}_{output_prefix}_{first_page_num:02d}",
                    )
            else:
                snapshot(
                    doc,
                    first_page_num,
                    output_dir,
                    f"{target_name}_{output_prefix}_{first_page_num:02d}",
                )
            if first_and_last_page:
                snapshot(
                    doc,
                    total_count - 1,
                    output_dir,
                    f"{target_name}_{output_prefix}_{total_count - 1:02d}",
                )
        else:
            if first_and_last_page:
                snapshot(doc, 0, output_dir, f"{target_name}_{output_prefix}_00")
            if first_and_last_page:
                for page_id in target_pages:
                    if page_id != 0 and page_id != total_count - 1:
                        snapshot(
                            doc,
                            page_id,
                            output_dir,
                            f"{target_name}_{output_prefix}_{page_id:02d}",
                        )
            else:
                for page_id in target_pages:
                    snapshot(
                        doc,
                        page_id,
                        output_dir,
                        f"{target_name}_{output_prefix}_{page_id:02d}",
                    )

            if first_and_last_page:
                snapshot(
                    doc,
                    doc.page_count - 1,
                    output_dir,
                    f"{target_name}_{output_prefix}_{total_count - 1:02d}",
                )


def process_social_security_pdf_beijing(
        pdf_path, target_name, output_dir="screenshots"
):
    process_social_security_pdf_base(pdf_path, target_name, output_dir, 10, 10, 20)


def process_social_security_pdf_nanjing(
        pdf_path, target_name, output_dir="screenshots"
):
    process_social_security_pdf_base(pdf_path, target_name, output_dir, 10, 10, 5)


def process_social_security_pdf_tianjin(
        pdf_path, target_name, output_dir="screenshots"
):
    process_social_security_pdf_base(
        pdf_path, target_name, output_dir, 10, 10, 15, False
    )


def process_social_security_pdf_chengdu(
        pdf_path, target_name, output_dir="screenshots"
):
    process_social_security_pdf_base(pdf_path, target_name, output_dir, 10, 10, 5)


def process_social_security_pdf_wuhan(pdf_path, target_name, output_dir="screenshots"):
    process_social_security_pdf_base(
        pdf_path, target_name, output_dir, 10, 10, 15, False
    )


def process_social_security_pdf_jinan(pdf_path, target_name, output_dir="screenshots"):
    process_social_security_pdf_base(
        pdf_path, target_name, output_dir, 10, 10, 5, False
    )


def process_social_security_pdf_fuzhou(pdf_path, target_name, output_dir="screenshots"):
    process_social_security_pdf_base(pdf_path, target_name, output_dir, 10, 10, 5)


def process_social_security_pdf_chongqing(
        pdf_path, target_name, output_dir="screenshots"
):
    process_social_security_pdf_base(pdf_path, target_name, output_dir, 10, 10, 5)


def process_social_security_pdf_dalian(pdf_path, target_name, output_dir="screenshots"):
    process_social_security_pdf_base(
        pdf_path, target_name, output_dir, 10, 10, 15, False
    )


"""
广东比较特殊， 一个月一张 PDF ， 所以输入是一个目录，包含广东的社保文件（最好只有这些文件，不要夹杂着其他文件 ）
然后按照名字能够排序，日期 从远到近 
"""


def guangzhou_process_loc(page):
    # 搜索目标姓名（支持模糊匹配，可根据实际调整）
    target_name = "该单位"
    text_instances = page.search_for(target_name)
    page_rect = page.rect
    page_width = page_rect.width

    if text_instances:
        # 给找到的文本添加红色框
        for rect in text_instances:
            # 调整矩形框大小，让框更美观（上下左右各扩展2个单位）
            # rect = fitz.Rect(rect.x0-X0_OFFSET, rect.y0-Y0_OFFSET,
            #                   page_rect.x1+X1_OFFSET, rect.y1+Y1_OFFSET)
            rect = fitz.Rect(rect.x0 - 3, rect.y0 - 3, rect.x1 + 60, rect.y1 + 10)
            # 添加红色框：width是框线宽度，color是RGB红色
            annot = page.add_rect_annot(rect)
            # annot = page.last_annot
            annot.set_colors(stroke=(1, 0, 0))  # 边框红色
            annot.set_border(width=BORDER_WIDTH)  # 边框宽度2px
            annot.update()


def process_social_security_pdf_guangdong(
        pdf_path, target_name, output_dir="screenshots"
):
    # 指定目录的Path对象
    directory = Path(pdf_path)
    pattern = "*.pdf"  # 通配符模式

    # 使用glob方法匹配文件
    matching_files = directory.glob(pattern)
    # matching_files.sort(key=lambda x: x.name)
    files = sorted(matching_files, key=lambda x: x.name)
    # 输出匹配的文件名
    for file in files:
        # print(file)
        name = file.name

        # fullname = file.absolute()
        fullname = os.path.join(pdf_path, name)
        process_social_security_pdf_base(
            fullname,
            target_name,
            output_dir,
            10,
            10,
            5,
            True,
            file.stem,
            guangzhou_process_loc,
        )


def test_beijing_ss():
    # 替换为你的PDF路径和要查找的人员姓名
    PDF_PATH = "data/example-beijing.pdf"  # 你的PDF文件路径
    # TARGET_NAME = "安京玲"  # 要查找的人员姓名

    # TARGET_NAME = "白首骏" # 白首骏 1  倪永哲 1 晋林涛 1
    OUTPUT_DIR = "screenshots"
    names = ["倪永哲", "晋林涛"]
    names = ["白首骏", "安京玲", "倪永哲", "晋林涛"]
    # 执行处理
    for name in names:
        output = f"{OUTPUT_DIR}/{name}"
        process_social_security_pdf_beijing(PDF_PATH, name, output)


def test_nanjing_ss():
    # 替换为你的PDF路径和要查找的人员姓名
    PDF_PATH = "data/example-nanjing-1.pdf"  # 你的PDF文件路径

    OUTPUT_DIR = "screenshots"
    names = ["张译文", "周洋", "祁海", "叶腾", "李嘉灏"]

    # 执行处理
    for name in names:
        output = f"{OUTPUT_DIR}/{name}"
        process_social_security_pdf_nanjing(PDF_PATH, name, output)


def test_tianjin_ss():
    # 替换为你的PDF路径和要查找的人员姓名
    PDF_PATH = "data/example-tianjin.pdf"  # 你的PDF文件路径

    OUTPUT_DIR = "screenshots"
    names = ["杨军锋", "丁凯", "李雪杰"]

    # 执行处理
    for name in names:
        output = f"{OUTPUT_DIR}/{name}"
        process_social_security_pdf_tianjin(PDF_PATH, name, output)


def test_chengdu_ss():
    # 替换为你的PDF路径和要查找的人员姓名
    PDF_PATH = "data/example-chengdu.pdf"  # 你的PDF文件路径

    OUTPUT_DIR = "screenshots"
    names = ["赵学平", "王友超"]

    # 执行处理
    for name in names:
        output = f"{OUTPUT_DIR}/{name}"
        process_social_security_pdf_chengdu(PDF_PATH, name, output)


def test_wuhan_ss():
    # 替换为你的PDF路径和要查找的人员姓名
    PDF_PATH = "data/example-wuhan.pdf"  # 你的PDF文件路径

    OUTPUT_DIR = "screenshots"
    names = ["邓超", "姚晶", "韩松明"]

    # 执行处理
    for name in names:
        output = f"{OUTPUT_DIR}/{name}"
        process_social_security_pdf_wuhan(PDF_PATH, name, output)


def test_jinan_ss():
    # 替换为你的PDF路径和要查找的人员姓名
    PDF_PATH = "data/example-jinan.pdf"  # 你的PDF文件路径

    OUTPUT_DIR = "screenshots"
    # names = ["周云状","马恒恒"     ]
    names = ["王", "张"]
    # 执行处理
    for name in names:
        output = f"{OUTPUT_DIR}/{name}"
        process_social_security_pdf_jinan(PDF_PATH, name, output)


def test_fuzhou_ss():
    # 替换为你的PDF路径和要查找的人员姓名
    PDF_PATH = "data/example-fuzhou.pdf"  # 你的PDF文件路径

    OUTPUT_DIR = "screenshots"
    # names = ["周云状","马恒恒"     ]
    names = ["吴建强", "林益峰"]
    # 执行处理
    for name in names:
        output = f"{OUTPUT_DIR}/{name}"
        process_social_security_pdf_fuzhou(PDF_PATH, name, output)


def test_chongqing_ss():
    # 替换为你的PDF路径和要查找的人员姓名
    PDF_PATH = "data/example-chongqing.pdf"  # 你的PDF文件路径

    OUTPUT_DIR = "screenshots"
    # names = ["周云状","马恒恒"     ]
    names = ["王朋", "陈维"]
    # 执行处理
    for name in names:
        output = f"{OUTPUT_DIR}/{name}"
        process_social_security_pdf_chongqing(PDF_PATH, name, output)


def test_guangdong_ss():
    # 替换为你的PDF路径和要查找的人员姓名
    PDF_PATH = "data/example-guangdong"  # 你的PDF文件路径

    OUTPUT_DIR = "screenshots"
    # names = ["周云状","马恒恒"     ]
    names = ["陈玉峰", "陈维"]
    # 执行处理
    for name in names:
        output = f"{OUTPUT_DIR}/{name}"
        process_social_security_pdf_guangdong(PDF_PATH, name, output)


def test_dalian_ss():
    # 替换为你的PDF路径和要查找的人员姓名
    PDF_PATH = "data/example-dalian.pdf"  # 你的PDF文件路径

    OUTPUT_DIR = "screenshots"
    # names = ["周云状","马恒恒"     ]
    names = ["许伟", "姜双双"]
    # 执行处理
    for name in names:
        output = f"{OUTPUT_DIR}/{name}"
        process_social_security_pdf_dalian(PDF_PATH, name, output)


def read_row_value_to_dict(row, column_names):
    current = {}
    for col in column_names:
        value = row[col]
        if pd.notna(value):
            current[col] = value
        else:
            current[col] = ""
    return current


def trim_all_names(names):
    out = []
    for name in names:
        out.append(name.strip())
    return out


def read_excel_sheet_values(file_name, sheet_name):
    df = pd.read_excel(file_name, sheet_name)
    out_list = []

    names = df.columns.tolist()
    # print(names)
    names = trim_all_names(names)
    for _, row in df.iterrows():
        one = read_row_value_to_dict(row, names)
        out_list.append(one)

    return out_list


CITY_DIRVERS = {
    "北京": process_social_security_pdf_beijing,
    "成都": process_social_security_pdf_chengdu,
    "大连": process_social_security_pdf_dalian,
    "福州": process_social_security_pdf_fuzhou,
    "广州": process_social_security_pdf_guangdong,
    "济南": process_social_security_pdf_jinan,
    "南京": process_social_security_pdf_nanjing,
    "天津": process_social_security_pdf_tianjin,
    "武汉": process_social_security_pdf_wuhan,
    "重庆": process_social_security_pdf_chongqing,
}


def read_and_process_from_excel(
        file_name, sheet_name, city_sheet_name, base_file_dir, output_dir
):
    city_files = {}
    cities = read_excel_sheet_values(file_name, city_sheet_name)
    for city in cities:
        city_name = city["City"]
        city_file = city["File"]
        if city_file is None or city_file == "":
            print("City file empty: ", city_name)
            continue
        city_files[city_name] = city_file

    users = read_excel_sheet_values(file_name, sheet_name)
    for user in users:
        name = user["Name"]
        city = user["City"]

        if city not in CITY_DIRVERS:
            print("Can't find city processor ", city, " , user ", name)
            continue

        if city not in city_files:
            print("Can't find city in `File` ", city, " , user ", name)
            continue

        file = city_files[city]

        if file == "":
            print("File empty, user ", name)
            continue

        fullname = os.path.join(base_file_dir, file)
        if not os.path.exists(fullname):
            print("File not found ", fullname, ", user ", name)
            continue

        processor = CITY_DIRVERS[city]
        # print(name, city, file)
        output = os.path.join(output_dir, name)
        processor(fullname, name, output)


if __name__ == "__main__——test":
    test_guangdong_ss()

if __name__ == "__main__":
    input_path = "./user-list.xlsx"
    output_file = "./output-user1.docx"
    template_file_name = "user_template.docx"
    read_and_process_from_excel(
        input_path,
        sheet_name="Users",
        city_sheet_name="Files",
        base_file_dir="data",
        output_dir="screenshots",
    )
