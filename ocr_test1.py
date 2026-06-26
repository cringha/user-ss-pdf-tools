import os
import paddle

paddle.set_flags({"FLAGS_eager_delete_tensor_gb": 0})
# paddle.set_flags({"use_mkldnn": False})
# 关闭 OneDNN 加速，解决兼容性报错
# os.environ["FLAGS_use_mkldnn"] = "0"

from paddleocr import PaddleOCR
# import paddle

# paddle.utils.run_check()

ocr = PaddleOCR(use_angle_cls=True, lang="ch")
result = ocr.predict("data/ocrtest1.png")

# 提取结果
for line in result:
    print(line)  # 文本内容
