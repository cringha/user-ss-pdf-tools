import re
from typing import List, Set, Tuple

import pdfplumber


# 基础配置


class SocialSecurityUser:
    def __init__(self, name: str, ss_id: str):
        self.name = name
        self.ss_id = ss_id

    def __str__(self):
        return f'{self.name}, {self.ss_id}'


def to_line(row) -> str:
    row_data = [cell.strip().replace("\n", "") if cell else "" for cell in row]
    s = []
    for it in row_data:
        if it is not None and it != "":
            s.append(it)
    return " ".join(s)


def common_extractor_(pdf_file) -> List[str]:
    """
    """
    line_list = []

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
                for row in table:
                    # 去除行内空值、空格
                    # row_data = [cell.strip().replace("\n","") if cell else "" for cell in row]
                    # str_data = " ".join(row_data)
                    # print(" ROW  " , row_data)
                    # print(" ROW- ", str_data)
                    line = to_line(row)
                    if line != "":
                        line_list.append(line)
    return line_list


def common_social_security_extractor(
        pdf_file: str, pattern: re.Pattern, key_index: int
) -> List[Tuple]:
    """
    解析福州社保PDF，提取参保人员姓名，过滤无效内容并去重
    """
    output = []
    lines = common_extractor_(pdf_file)

    exist_keys = set()

    for index, line in enumerate(lines, start=1):
        print(f"行号: {index}, 内容: {line}")
        ll = line.strip()
        match = pattern.match(ll)
        if match:
            groups = match.groups()

            key = groups[key_index]
            if key not in exist_keys:
                exist_keys.add(key)
                output.append(groups)
            else:
                print(f"key_index: {key_index}  key: {key} exist")
        else:
            print(f" Not match >>>{ll}<<<")

        # for match in pattern.finditer(line):
        #     groups = match.groups()
        #
        #     key = groups[key_index]
        #     if key not in exist_keys:
        #         exist_keys.add(key)
        #         output.append(groups)

        # for match in pattern.finditer(line):
        #     groups = match.groups()
        #
        #     key = groups[key_index]
        #     if key not in exist_keys:
        #         exist_keys.add(key)
        #         output.append(groups)
    return output


def common_social_security_extractor_old(
        pdf_file: str, pattern: re.Pattern
) -> List[Tuple]:
    """
    解析福州社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    output = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            # 提取页面所有表格
            print(
                f"Page :{page.page_number}, file :{pdf_file}",
            )

            lines = page.extract_text_lines()
            if not lines:
                continue

            # print("lines ", len(lines))
            for index, line in enumerate(lines, start=1):
                tt = line["text"]

                print(f"行号: {index}, 内容: {tt}")
                for match in pattern.finditer(tt):
                    groups = match.groups()
                    output.append(groups)
                    # seq, id_num, name = match.groups()

        return output


from typing import Callable
import fitz  # PyMuPDF，用于PDF处理
import os

BORDER_WIDTH = 4


def snapshot(doc, page_num, filename, user_name, pdf_filename):
    # 2. 截取首页（第一个包含目标人员的页面）
    first_page = doc[page_num]
    # 将页面转为图片（分辨率300dpi，保证清晰度）
    mat = fitz.Matrix(300 / 72, 300 / 72)
    first_pix = first_page.get_pixmap(matrix=mat)
    first_pix.save(filename)
    print(f"已保存：{user_name}, {filename}, {pdf_filename}")


def snapshot1(doc, page_num, output_dir, filename):
    # 2. 截取首页（第一个包含目标人员的页面）
    first_page = doc[page_num]
    # 将页面转为图片（分辨率300dpi，保证清晰度）
    mat = fitz.Matrix(300 / 72, 300 / 72)
    first_pix = first_page.get_pixmap(matrix=mat)
    png_name = f"{filename}.png"
    first_pix.save(os.path.join(output_dir, png_name))
    print(f"截图已保存：{png_name}")


def snapshot_user_social_security_info_pdf_base(
        pdf_path,
        user_name,
        left_offset=10,
        right_offset=10,
        height_offset=20,
        first_and_last_page=True,
        filename_callback: Callable[[int], str] = None,
        fn_process=None,
) -> bool:
    """
    处理社保PDF文件，定位指定人员并截图（首页/尾页），人员信息加红框

    Args:
        :param filename_callback: 函数，生成文件名
        :param first_and_last_page: 是否要截取首页及尾页
        :param pdf_path:  PDF文件路径
        :param user_name: 要定位的人员姓名
        :param height_offset: 狂徒的高度
        :param right_offset: 画框框的右边的 offset 像素位置，一般是整个页面宽度
        :param left_offset: 画框框的左边的 offset 像素位置
    """

    # print("Process ", pdf_path)

    # 打开PDF文件
    doc = fitz.open(pdf_path)
    if doc.page_count == 0:
        print("PDF文件为空，无法处理, {pdf_path}")
        return False

    # 存储包含目标人员的页面编号
    target_pages = []
    rect_list = []  # 存储目标人员位置的矩形框

    # 1. 遍历PDF页面，查找目标人员并添加红色框
    for page_num in range(doc.page_count):
        page = doc[page_num]

        if fn_process is not None:
            fn_process(page)

        # 搜索目标姓名（支持模糊匹配，可根据实际调整）
        text_instances = page.search_for(user_name)
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
        print(f"未找到：{user_name}, {pdf_path}")
        return False

    total_count = doc.page_count
    if total_count == 1:  # 就一页，直接截图
        filename = filename_callback(0)  # f"{target_name}_{output_prefix}_00"
        snapshot(doc, 0, filename, user_name, pdf_path)
    else:
        if len(target_pages) == 1:
            first_page_num = target_pages[0]

            if first_and_last_page:
                filename = filename_callback(0)  # f"{target_name}_{output_prefix}_00"
                snapshot(doc, 0, filename, user_name, pdf_path)

            if first_and_last_page:
                if first_page_num != 0 and first_page_num != total_count - 1:
                    filename = filename_callback(
                        first_page_num)  # f"{target_name}_{output_prefix}_{first_page_num:02d}",
                    snapshot(
                        doc,
                        first_page_num,
                        filename, user_name, pdf_path
                    )
            else:
                filename = filename_callback(first_page_num)  # f"{target_name}_{output_prefix}_{first_page_num:02d}",
                snapshot(
                    doc,
                    first_page_num,
                    filename, user_name, pdf_path
                )
            if first_and_last_page:
                filename = filename_callback(total_count - 1)  # f"{target_name}_{output_prefix}_{total_count - 1:02d}"
                snapshot(
                    doc,
                    total_count - 1,
                    filename, user_name, pdf_path
                )
        else:
            if first_and_last_page:
                filename = filename_callback(0)  # f"{target_name}_{output_prefix}_00"
                snapshot(doc, 0, filename, user_name, pdf_path)
            if first_and_last_page:
                for page_id in target_pages:
                    if page_id != 0 and page_id != total_count - 1:
                        filename = filename_callback(page_id)  # f"{target_name}_{output_prefix}_{page_id:02d}"
                        snapshot(
                            doc,
                            page_id,
                            filename, user_name, pdf_path
                        )
            else:
                for page_id in target_pages:
                    filename = filename_callback(page_id)  # f"{target_name}_{output_prefix}_{page_id:02d}"
                    snapshot(
                        doc,
                        page_id,
                        filename, user_name, pdf_path
                    )

            if first_and_last_page:
                filename = filename_callback(
                    doc.page_count - 1)  # f"{target_name}_{output_prefix}_{total_count - 1:02d}"
                snapshot(
                    doc,
                    doc.page_count - 1,
                    filename, user_name, pdf_path
                )
    return True


NAMES = ["北京", "beijing"]


class AbstractParser:
    def __init__(self, *args, **kwargs) -> None:

        if "output_dir" in kwargs:
            self.output_dir = kwargs["output_dir"]
        else:
            self.output_dir = "screenshots"

    def get_city_names(self) -> List[str]:
        pass

    def match_city_name(self, name: str) -> bool:
        names = self.get_city_names()
        for loc_name in names:
            if name in loc_name:
                return True
        return False

    def match_file_name(self, file_name: str) -> bool:
        names = self.get_city_names()
        for loc_name in names:
            if loc_name in file_name:
                return True
        return False

    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        pass

    def snapshot_user(self, file_name: str, user_name: str, target_name: str = None) -> bool:
        pass

    def snapshot_user_base(self, file_name: str, user_name: str,
                           target_name: str = None,
                           left_offset=10,
                           right_offset=10,
                           height_offset=20,
                           first_and_last_page=True, cb_process_pre_page=None, cb_gen_file_name=None) -> bool:

        full_path = os.path.join(self.output_dir, user_name)

        # 创建输出目录
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        loc_gen_file_name = cb_gen_file_name

        def gen_file_name(page_num: int) -> str:
            name = f"{user_name}-社保-{page_num:02d}.png"
            return os.path.join(full_path, name)

        if loc_gen_file_name is None:
            loc_gen_file_name = gen_file_name

        if target_name is None:
            target_name = user_name

        return snapshot_user_social_security_info_pdf_base(file_name, target_name,
                                                           left_offset, right_offset,
                                                           height_offset, first_and_last_page, loc_gen_file_name,
                                                           cb_process_pre_page)
