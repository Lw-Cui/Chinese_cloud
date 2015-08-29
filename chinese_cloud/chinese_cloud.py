from random import Random, random
from integral_occupancy_map import IntegralOccupancyMap
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import jieba
import numpy
import codecs
import os
import re

STOPWORDS = set([x.strip() for x in
                 codecs.open(os.path.join(os.path.dirname(__file__), 'stopwords'), encoding='utf8').read().split('\n')])


class ChineseCloud(object):

    def __init__(self, width=600, height=300, max_font=80, min_font=30):
        self.width = width
        self.height = height
        self.max_font = max_font
        self.min_font = min_font
        self.image = None
        self.frequencies = None
        self.layout = None
        self.stopwords = STOPWORDS

    def get_count(self, seg_list):
        is_word = re.compile(ur'^([\w|\u4e00-\u9fa5])+$')

        word_list = {}
        for word in seg_list:
            if is_word.match(word) and word not in self.stopwords:
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
        font_sizes, positions, orientations, colors = [], [], [], []
        for word, fre in self.frequencies:
            font_size = int(fre / last_fre * self.max_font)
            orientation = None

            result = None
            while True:
                font = ImageFont.truetype('DroidSansFallbackFull.ttf', font_size)
                if random() < 0.95:
                    orientation = None
                else:
                    orientation = Image.ROTATE_90
                transposed_font = ImageFont.TransposedFont(font, orientation=orientation)
                draw.setfont(transposed_font)
                box_size = draw.textsize(word)
                result = occupancy.sample_position(box_size[1], box_size[0], Random())
                if result is not None or font_size < self.min_font:
                    break
                font_size -= 2

            if font_size < self.min_font:
                break
            x, y = numpy.array(result)
            draw.text((y, x), word, fill='white')
            occupancy.update(numpy.asarray(self.image), x, y)
            positions.append((x, y))
            orientations.append(orientation)
            font_sizes.append(font_size)
            colors.append("hsl(%d, 80%%, 50%%)" % Random().randint(0, 255))
            last_fre = fre

        self.layout = list(zip(self.frequencies, font_sizes, positions, orientations, colors))
        return self

    def generate(self, text):
        seg_list = jieba.cut(text)
        count = self.get_count(seg_list)
        self.set_frequencies(count).generate_pic()
        return self

    def to_image(self, filename):
        img = Image.new('RGB', (self.width, self.height), 'white')
        draw = ImageDraw.Draw(img)
        for (word, count), font_size, position, orientation, color in self.layout:
            font = ImageFont.truetype('DroidSansFallbackFull.ttf', font_size)
            transposed_font = ImageFont.TransposedFont(font, orientation=orientation)
            draw.setfont(transposed_font)
            pos = (position[1], position[0])
            draw.text(pos, word, fill=color)
        img.show()
        img.save(filename)
        return self
