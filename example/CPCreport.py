#!/usr/bin/env python2

from os import path
from chinese_cloud.chinese_cloud import ChineseCloud

text_dir = path.dirname(__file__)
#text = open(path.join(text_dir, 'constitution.txt')).read()
text = open(path.join(text_dir, 'article')).read()
chinese_cloud = ChineseCloud(width=800, height=400, max_font=100, min_font=20).generate(text).to_image('report.png')
