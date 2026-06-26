import pytesseract


langs = pytesseract.get_languages()
print(langs)

# out = pytesseract.image_to_alto_xml("data/ocrtest1.png", lang="chi_sim")
# print(out)
# 打开文件以写入二进制模式
# with open("test.xml", "wb") as file:
#     file.write(out)
