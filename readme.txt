安装： 
openpyxl
PyMuPDF
pdfplumber
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple docxtpl jinja2 pdfplumber PyMuPDF pyinstaller




使用：

python export_user_ss_snapshots.py

社保PDF转用户截图工具

options:
  -h, --help            show this help message and exit
  -i INPUT_XLSX, --input-xlsx INPUT_XLSX
                        输入Xlsx文件
  -p PDF_ROOT, --pdf-root PDF_ROOT
                        输入PDF文件根目录
  -s SNAPSHOT_IMAGES, --snapshot-images SNAPSHOT_IMAGES
                        输出截图文件根目录
  --sheet-name-user SHEET_NAME_USER
                        User sheet name
  --sheet-name-file SHEET_NAME_FILE
                        File sheet name
  -c, --convert         将截图转换为DOCX文档
  -t DOCX_TEMPLATE_FILE, --docx-template-file DOCX_TEMPLATE_FILE
                        docx template filename
  -o OUTPUT_DOCX_FILE, --output-docx-file OUTPUT_DOCX_FILE
                        输出docx文件




python export_user_ss_snapshots.py -i test_data\user-list.xlsx  -p test_data\
