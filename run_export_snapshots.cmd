@call .venv\Scripts\activate.bat

chcp 65001

REM 输入的Excel数据，按照格式填写数据
SET INPUT_EXCEL=test_data\user-list.xlsx

REM 输入 社保PDF文件的根目录，每个城市的社保，按照约定的城市命名，例如：“北京.pdf”
SET INPUT_SS_DATA_ROOT=.\data

REM 输出，社保截图文件的存放位置
SET OUTPUT_IMAGE_ROOT=.\output

python export_user_ss_snapshots.py -i %INPUT_EXCEL%  -p %INPUT_SS_DATA_ROOT% --snapshot-images %OUTPUT_IMAGE_ROOT%

@call .venv\Scripts\deactivate.bat