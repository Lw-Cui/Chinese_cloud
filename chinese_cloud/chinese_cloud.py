import jieba
import numpy
import re


class ChineseCloud(object):

    def get_frequencies(self, seg_list):
        is_word = re.compile(ur'^([\w|\u4e00-\u9fa5])+$')

        word_list = {}
        for word in seg_list:
            if is_word.match(word):
                word_list[word] = word_list.get(word, 0) + 1
        return word_list

    def generate_pic(self, frequencies):
        frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        max_frequencies = float(numpy.max([fre for key, fre in frequencies]))
        for i, (key, fre) in enumerate(frequencies):
            frequencies[i] = key, fre / max_frequencies

    def generate(self, text):
        seg_list = jieba.cut(text)
        frequencies = self.get_frequencies(seg_list)
        self.generate_pic(frequencies)
