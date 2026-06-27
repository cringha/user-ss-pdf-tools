from pathlib import Path
import argparse
import pandas as pd
import os

from parser.parser_manager import get_city_cf_by_name, get_processor_by_city_name
from uitls.convert_image_to_docx import convert_user_ss_snapshot_images_to_docx
from uitls.excel_utils import read_excel_sheet_values


def get_last_by_filename_glob(directory, pattern="*"):
    dir_path = Path(directory)
    # 获取所有匹配的文件（排除子目录）
    files = [f for f in dir_path.glob(pattern)]

    if not files:
        print("未找到匹配的文件")
        return None

    # 按文件名（字符串）升序排序，取最后一个
    files_sorted = sorted(files, key=lambda f: f.name)
    return files_sorted

#
# def parse_one_file(file: Path, file_type: str):
#     if file_type is None or file_type == "":
#         file_type = guess_city_key_by_filename(file.name)
#
#     if file_type is None or file_type == "":
#         print(f"Can't check file_type by {file.name}")
#         return []
#
#     output = []
#     names = parser_ss_file(file_type, str(file))
#     for name in names:
#         # print(name)
#         one = {"name": name.name, "file_type": file_type, "file": file.name}
#         output.append(one)
#     return output


# def parse_multi_files(files1, file_type: str):
#     output = []
#     for file in files1:
#         one = parse_one_file(file, file_type)
#         if one is not None:
#             output.extend(one)
#     return output


def save_names(records, file_name):
    df = pd.DataFrame(records)
    print(f"成功提取 {len(df)} 条记录：")
    print(df.to_string(index=False))

    # 保存完整记录

    df.to_csv(file_name, index=False, encoding="utf-8-sig")
    print(f"\n完整记录已保存至：{file_name}")


def read_and_process_from_excel(base_pdf_file_dir, output_image_dir,
                                excel_file_name, user_sheet_name="Users", city_sheet_name="Files",
                                col_user_name="Name", col_city_name="City", col_file_name="File"
                                ):
    city_files = {}
    cities = read_excel_sheet_values(excel_file_name, city_sheet_name)
    for city in cities:
        city_name = city[col_city_name]
        city_file = city[col_file_name]
        if city_file is None or city_file == "":
            print("City file empty: ", city_name)
            continue
        if city_name not in city_files:
            city_files[city_name] = []
        city_files[city_name].append(city_file)

    city_processor = {}

    users = read_excel_sheet_values(excel_file_name, user_sheet_name)
    user_list = []
    for user in users:
        user_name = user[col_user_name]
        city = user[col_city_name]
        user_list.append(user_name)
        city_cf = get_city_cf_by_name(city)
        if city_cf is None:
            print("Can't find city processor ", city, " , user ", user_name)
            continue

        if city not in city_files:
            print("Can't find city in `File` ", city, " , user ", user_name)
            continue

        city_file_list = city_files[city]

        if city_file_list is None or len(city_file_list) == 0:
            print("City file empty, city ", city)
            continue

        if city not in city_processor:
            processor = get_processor_by_city_name(city, output_dir=output_image_dir)
            city_processor[city] = processor

        processor = city_processor[city]
        # print(name, city, file)

        for city_file in city_file_list:
            full_file_name = os.path.join(base_pdf_file_dir, city_file)
            if not os.path.exists(full_file_name):
                print("File not found ", full_file_name, ", user ", user_name)
                continue

            result1 = processor.snapshot_user(full_file_name, user_name)
            if result1:
                break
    return user_list


def main(args):
    if args.input_xlsx is None or args.input_xlsx == "":
        print("--input-xlsx 空")

        return False

    if args.pdf_root is None or args.pdf_root == "":
        print("--pdf-root 空")
        return False

    user_list = read_and_process_from_excel(args.pdf_root,
                                            args.snapshot_images,
                                            args.input_xlsx,
                                            args.sheet_name_user,
                                            args.sheet_name_file
                                            )

    if args.convert:
        convert_user_ss_snapshot_images_to_docx(user_list, args.snapshot_images, args.docx_template_file,
                                            args.output_docx_file)
    return True


if __name__ == "__main__":

    #
    parser = argparse.ArgumentParser(description="社保PDF转用户截图工具")
    parser.add_argument("-i", "--input-xlsx", help="输入Xlsx文件")
    parser.add_argument("-p", "--pdf-root", help="输入PDF文件根目录")
    parser.add_argument("-s", "--snapshot-images", help="输出截图文件根目录", default="./output")
    parser.add_argument("--sheet-name-user", help="User sheet name", default="Users")
    parser.add_argument("--sheet-name-file", help="File sheet name", default="Files")
    parser.add_argument("-c", "--convert", action="store_true", help="将截图转换为DOCX文档")
    parser.add_argument("-t", "--docx-template-file", help="docx template filename",
                        default="./data/user_ss_template.docx")
    parser.add_argument("-o", "--output-docx-file", help="输出docx文件", default="./user-ss-snapshot.docx")
    # parser.add_argument("-h", "--help", help="打印参数信息")

    args = parser.parse_args()

    result = main(args)
    if not result:
        parser.print_help()
