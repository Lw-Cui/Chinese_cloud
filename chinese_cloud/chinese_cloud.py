from random import Random
from integral_occupancy_map import IntegralOccupancyMap
import Image
import ImageDraw
import ImageFont
import jieba
import numpy
import re


class ChineseCloud(object):

    def __init__(self, width=600, height=300, max_font=100, min_font=30):
        self.width = width
        self.height = height
        self.max_font = max_font
        self.min_font = min_font
        self.image = None
        self.frequencies = None

    @staticmethod
    def get_count(seg_list):
        is_word = re.compile(ur'^([\w|\u4e00-\u9fa5])+$')

        word_list = {}
        for word in seg_list:
            if is_word.match(word):
                word_list[word] = word_list.get(word, 0) + 1
        return word_list

    def set_frequencies(self, count):
        count = sorted(count.items(), key=lambda x: x[1], reverse=True)
        max_frequencies = float(numpy.max([fre for key, fre in count]))
        for i, (key, fre) in enumerate(count):
            count[i] = key, fre / max_frequencies
        self.frequencies = count
        return self

    def generate_pic(self):
        self.image = Image.new('L', (self.width, self.height))

        draw = ImageDraw.ImageDraw(self.image)
        occupancy = IntegralOccupancyMap(self.height, self.width)
        last_fre = 1.0
        for word, fre in self.frequencies:
            font_size = int(fre / last_fre * self.max_font)

            result = None
            while True:
                font = ImageFont.truetype('DroidSansFallbackFull.ttf', font_size)
                draw.setfont(font)
                box_size = draw.textsize(word)
                result = occupancy.sample_position(box_size[1], box_size[0], Random())
                if result is not None or font_size < self.min_font:
                    break
                font_size -= 2

            if result is None:
                return self
            elif font_size < self.min_font:
                break
            x, y = numpy.array(result)
            draw.text((y, x), word, fill='red')
            occupancy.update(numpy.asarray(self.image), x, y)
            last_fre = fre
        return self

    def generate(self, text):
        seg_list = jieba.cut(text)
        count = self.get_count(seg_list)
        self.set_frequencies(count).generate_pic()
        return self

    def to_image(self, filename):
        #self.image.save(filename)
        self.image.show()
        return self
