import os
from docx.shared import Mm
from jinja2 import Environment
from pathlib import Path

from pathlib import Path
import os
import pandas as pd


import fitz  # PyMuPDF，用于PDF处理

from docxtpl import DocxTemplate, InlineImage


class UserSSImages:
    def __init__(self, name: str):
        self.name = name
        self.images = []
        self.ssImages = []

    def add(self, v):
        self.images.append(v)


def enum_all_user_certs(user: UserSSImages, source_dir: str = "./"):
    # 转换为Path对象，方便路径操作
    dir_path = Path(source_dir)
    # 筛选目录下所有PNG文件（不区分大小写，如.png/.PNG）
    png_files = [
        file
        for file in dir_path.iterdir()
        if file.is_file() and file.suffix.lower() == ".png"
    ]

    # 按文件名排序（确保ID顺序固定）
    png_files.sort(key=lambda x: x.name)

    user_certs = {}

    # 遍历文件并添加ID重命名
    for idx, file in enumerate(png_files, start=1):  # ID从1开始递增
        full_name = os.path.join(source_dir, file.name)
        user.add(full_name)
        # # cert_name = tp[0:-1]
    return user_certs


image_size = 150


def pre_process_user_image_obj(tpl, user):

    for u in user.images:
        image = InlineImage(tpl, u, width=Mm(image_size))
        user.ssImages.append(image)


def enum_all_users(source_dir: str = "./"):
    # 转换为Path对象，方便路径操作
    dir_path = Path(source_dir)
    # 筛选目录下所有PNG文件（不区分大小写，如.png/.PNG）
    user_dirs = [file.name for file in dir_path.iterdir() if file.is_dir()]
    return user_dirs


def read_user_ss_images_to_docx(users, snapshots, template_path, output_file=""):

    all_users = []

    docx = DocxTemplate(template_path)

    for user in users:
        user_image_base = f"{snapshots}/{user}"
        if not os.path.exists(user_image_base):
            print(f"Use : {user} not exist ")
            continue

        u = UserSSImages(user)
        all_users.append(u)

        enum_all_user_certs(u, user_image_base)
        pre_process_user_image_obj(docx, u)
    obj = {"users": all_users}

    jinja_env = Environment()
    # jinja_env.globals['user_project_exp'] = user_project_exp

    # 获取要插入到文档中的数据
    # 渲染文档
    docx.render(obj, jinja_env)
    # 保存生成的文档
    docx.save(output_file)


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


def read_name_from_excel(file_name, sheet_name):
    output = []
    users = read_excel_sheet_values(file_name, sheet_name)
    for user in users:
        name = user["Name"]
        # city = user["City"]

        output.append(name)
    return output


if __name__ == "__main__":
    OUTPUT_DIR = "screenshots"
    # names = ["白首骏", "安京玲", "倪永哲", "晋林涛"]

    input_path = "./user-list.xlsx"
    output_file = "./output-user1.docx"

    # names = enum_all_users(OUTPUT_DIR)
    names = read_name_from_excel(input_path, "Users")

    output_file = "./output-user-ss-images.docx"
    template_file_name = "./data/user_ss_template.docx"
    read_user_ss_images_to_docx(
        names, OUTPUT_DIR, template_path=template_file_name, output_file=output_file
    )
