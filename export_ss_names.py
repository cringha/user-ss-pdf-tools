from pathlib import Path
import argparse
import pandas as pd


from parser.parser_manager import guess_city_key_by_filename, parser_ss_file


def get_last_by_filename_glob(directory, pattern="*"):

    dir_path = Path(directory)
    # 获取所有匹配的文件（排除子目录）
    files = [f for f in dir_path.glob(pattern) ]

    if not files:
        print("未找到匹配的文件")
        return None

    # 按文件名（字符串）升序排序，取最后一个
    files_sorted = sorted(files, key=lambda f: f.name)
    return files_sorted



def parse_one_file( file: Path , file_type:str ):
    if file_type is None or file_type == "":

        file_type = guess_city_key_by_filename( file.name)

    if file_type is None or file_type == "":
        print(f"Can't check file_type by {file.name }")
        return []

    output = []
    names = parser_ss_file( file_type, str(file) )
    for name in names:
        # print(name)
        one = { "name": name.name , "file_type": file_type , "file" : file.name}
        output.append(one)
    return output



def parse_multi_files( files1,  file_type:str  ):
    output = []
    for file in files1:
        one = parse_one_file( file, file_type)
        if one is not None:
            output.extend( one )
    return output



def save_names(records, file_name ):
    df = pd.DataFrame(records)
    print(f"成功提取 {len(df)} 条记录：")
    print(df.to_string(index=False))

    # 保存完整记录

    df.to_csv(file_name, index=False, encoding="utf-8-sig")
    print(f"\n完整记录已保存至：{file_name}")



if __name__ == "__main__":

    default_current_path = "./"

    parser = argparse.ArgumentParser(description="示例工具")
    parser.add_argument("-i", "--input", help="输入文件通配符",default="./*.pdf")
    parser.add_argument("-t", "--type", help="输入文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径")
    args = parser.parse_args()

    files = get_last_by_filename_glob(default_current_path, args.input )
    if files is None:
        print(f"Found empty files, {args.input}")
    else:
        output_list  = parse_multi_files(files, args.type)
        if args.output is not None:
            save_names( output_list, args.output )
        else:
            for name in output_list:
                print(name)

        # OUTPUT_DIR = "screenshots"
        # # names = ["白首骏", "安京玲", "倪永哲", "晋林涛"]
        #
        # input_path = "./user-list.xlsx"
        # output_file = "./output-user1.docx"

