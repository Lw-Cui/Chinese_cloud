#!/usr/bin/env python2

from os import path
from chinese_cloud.chinese_cloud import ChineseCloud

text_dir = path.dirname(__file__)
text = open(path.join(text_dir, 'article')).read()
chinese_cloud = ChineseCloud(width=1000, height=600, max_font=200, min_font=20).generate(text).to_image('a')
