import re
from typing import List
import os
from parser.common.parser_common import common_social_security_extractor, SocialSecurityUser, AbstractParser
from typing import Callable
import fitz  # PyMuPDF，用于PDF处理
import os

BORDER_WIDTH = 4


def extract_social_security_guangdong(pdf_file) -> List[SocialSecurityUser]:
    """
     社保PDF，提取参保人员姓名，过滤无效内容并去重
    """

    filter_words = {"单位", "个人"}

    # 序号 职工姓名 公民身份号码 基本养老保险 工伤保险 失业保险、
    # 1 蒋辉 341221199208013496

    s = r"(\d+)\s+([\u4e00-\u9fa5]+)\s+([0-9Xx]{18})(.*)"

    pattern = re.compile(s)
    output = []
    items = common_social_security_extractor(pdf_file, pattern, 1)
    num = 0
    for item in items:
        num, name, id_num, *_ = item
        if name in filter_words:
            print(" name in filter list , ignore ", name)
        else:
            print(f"No{num} - User {name}, id:{id_num}")
            u = SocialSecurityUser(name, id_num)
            output.append(u)

    return output


from pathlib import Path


def get_sorted_filename_list(directory, pattern="*"):
    """
    按文件名升序排序，取最后一个
    :param directory: 目录路径
    :param pattern: 通配符模式，如 '*.log', 'report_*'
    """
    dir_path = Path(directory)
    # 获取所有匹配的文件（排除子目录）
    files = [f for f in dir_path.glob(pattern) if f.is_file()]

    if not files:
        print("未找到匹配的文件")
        return None

    # 按文件名（字符串）升序排序，取最后一个
    files_sorted = sorted(files, key=lambda f: f.name)
    return files_sorted

def get_last_by_filename_glob(directory, pattern="*"):

    files_sorted = get_sorted_filename_list( directory, pattern )
    if not files_sorted and len(files_sorted) > 0:
        return files_sorted[-1]
    return None




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




class GuangDongParser(AbstractParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_city_names(self) -> List[str]:
        return ["广东","广州"]


    def parse_file(self, file_name: str) -> List[SocialSecurityUser]:
        file = get_last_by_filename_glob(file_name, pattern="*.pdf")
        if file is None:
            raise FileNotFoundError(file_name)
        return extract_social_security_guangdong(file)

    def snapshot_user(self, pdf_path: str, user_name: str, target_name: str = None):

        # 指定目录的Path对象
        # 指定目录的Path对象
        files = get_sorted_filename_list(pdf_path, "*.pdf")

        full_path = os.path.join(self.output_dir, user_name)


        # 输出匹配的文件名
        for file in files:
            # print(file)
            name = file.name

            def guangdong_gen_file_name(page_num: int) -> str:
                name3 = f"{user_name}-社保-{file.stem}-{page_num:02d}.png"
                return os.path.join(full_path, name3)

            # fullname = file.absolute()
            fullname = os.path.join(pdf_path, name)
            self.snapshot_user_base(fullname,
                                    user_name, target_name, 10, 10, 5,
                                    True,guangzhou_process_loc, guangdong_gen_file_name)
            # process_social_security_pdf_base(
            #     fullname,
            #     target_name,
            #     output_dir,
            #     10,
            #     10,
            #     5,
            #     True,
            #     file.stem,
            #     guangzhou_process_loc,
            # )

        return True
