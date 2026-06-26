from pathlib import Path


def get_last_by_filename_glob(directory, pattern="*"):
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
    return files_sorted[-1]


if __name__ == "__main__":
    OUTPUT_DIR = "screenshots"
    # names = ["白首骏", "安京玲", "倪永哲", "晋林涛"]

    input_path = "./user-list.xlsx"
    output_file = "./output-user1.docx"

