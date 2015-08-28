__author__ = 'lw'

from os import path

from chinese_cloud.chinese_cloud import ChineseCloud

text_dir = path.dirname(__file__)
text = open(path.join(text_dir, 'article')).read()
chinese_cloud = ChineseCloud().generate(text)
