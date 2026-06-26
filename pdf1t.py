import fitz  # PyMuPDF

def search_pdf_text(pdf_path, search_text):
    # 打开PDF文件
    doc = fitz.open(pdf_path)
    results = []
    index = 0 
    # 遍历每一页
    for page in doc:
        # 获取当前页的文本及其位置信息
        text_items = page.get_text("dict")
        if text_items:
            blocks = text_items["blocks"]
            if blocks:
                for block in blocks:
                    print("block lines ", index )
                    index = index + 1
                    lines = block["lines"]
                    if lines:
                        for line in lines:
                            spans = line["spans"]
                            if spans:
                                for span in spans:
                                    text = span["text"]
                                    if text:
                                        if search_text in text:
                                            # 记录文本及其位置信息
                                            results.append({
                                                "text": span["text"],
                                                "position": (span["bbox"][0], span["bbox"][1]),  # 文本左上角的位置
                                                "page": page.number + 1  # 页码从1开始
                                            })
    doc.close()
    return results

# 使用函数
pdf_path = 'data/example1.pdf'
search_text = '你想要搜索的文字'
found_texts = search_pdf_text(pdf_path, search_text)
for result in found_texts:
    print(f'Text: "{result["text"]}", Position: {result["position"]}, Page: {result["page"]}')
