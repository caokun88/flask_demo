# coding=utf8
# create by caokun on 2017-06-26

import os
import random
import string

from django.conf import settings

from PIL import Image, ImageDraw, ImageFont, ImageFilter


IMAGE_MODE = 'RGB'
IMAGE_SIZE = (105, 37)
IMAGE_COLOR = (255, 255, 255)
FONT_SIZE = 30


def _rand_list(length):
    """
    验证码随机字符
    :param length:
    :return:
    """
    return random.sample(string.letters + string.digits, length)


def _rand_color():
    """
    随机颜色
    :return:
    """
    return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)


def _create_lines(draw, count):
    for i in range(count):
        begin = (random.randint(0, IMAGE_SIZE[0]), random.randint(0, IMAGE_SIZE[1]))
        end = (random.randint(0, IMAGE_SIZE[0]), random.randint(0, IMAGE_SIZE[1]))
        draw.line([begin, end], fill=(0, 0, 0))


def _create_points(draw):
    for w in range(IMAGE_SIZE[0]):
        for h in range(IMAGE_SIZE[1]):
            # draw.point((x, y), fill=rndColor())
            if random.randint(0, 50) > 45:
                draw.point((w, h), fill=(0, 0, 0))


def generate_captcha():
    image = Image.new(IMAGE_MODE, IMAGE_SIZE, IMAGE_COLOR)
    front_file = os.path.join(settings.BASE_DIR, 'dj_demo/fonts/Arial.ttf')
    font = ImageFont.truetype(front_file, FONT_SIZE)
    draw = ImageDraw.Draw(image)
    rand_str = ''.join(_rand_list(4))
    draw.text((0, 0), rand_str, fill=_rand_color(), font=font)
    _create_points(draw)
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    image = image.transform(IMAGE_SIZE, Image.PERSPECTIVE, params)  # 创建扭曲

    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）
    return image


if __name__ == '__main__':
    image = generate_captcha()
    print image

