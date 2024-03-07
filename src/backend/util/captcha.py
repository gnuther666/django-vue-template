import random, uuid
from string import digits, ascii_letters
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from typing import Dict

class Captcha:

    def __generate_captcha_text(self, len=4):
        chars = digits + ascii_letters
        return ''.join(random.choices(chars, k=len))
    def __create_captcha_image(self, text, width=200, height=50, font_path='./util/arial.ttf'):
        """根据验证码文本生成图片"""
        font_size = int(height * 0.8)
        image = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)

        # 加载字体
        font = ImageFont.truetype(font_path, font_size)
        print(font.font.getsize(text))


        # 计算并绘制文本
        text_width, text_height = font.font.getsize(text)
        margin = int(height * 0.1)  # 增加文本边距
        x = (width - text_width[1] - margin * 2) // 2
        y = (height - text_height[1] - margin * 2) // 2
        draw.text((x, y  - text_height[1]), text, fill=(0, 0, 0), font=font)

        # 可以添加一些干扰线和点以增加识别难度
        for _ in range(3):
            draw.line([(random.randint(0, width), random.randint(0, height)),
                       (random.randint(0, width), random.randint(0, height))], fill=(0, 0, 0))
            draw.point([random.randint(0, width), random.randint(0, height)], fill=(0, 0, 0))

        return image
    
    def get_captcha(self) -> Dict[str, str]:
        """
        视图函数，返回验证码图片及文本
        返回:
        Dict[str, str]: 一个具有三个键值对的字典：
            - 'out_buff': 验证码图片的十六进制字符串
            - 'captcha_text': 验证码中的文字
            - 'key': 验证码的键值，用于redis入库
        """
        key = uuid.uuid4().hex
        captcha_text = self.__generate_captcha_text()
        captcha_image = self.__create_captcha_image(captcha_text)

        # # 将验证码存入session以便后续验证
        # request.session['captcha'] = captcha_text.lower()

        # 转为BytesIO对象以便HTTP响应
        output_buffer = BytesIO()
        captcha_image.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        image_data = output_buffer.read()
        hex_string = image_data.hex()
        # response = HttpResponse(content_type="image/png")
        # response.write(output_buffer.read())
        # return response    
        return {'out_buff': hex_string, 'captcha_text': captcha_text.lower(), 'key': key}