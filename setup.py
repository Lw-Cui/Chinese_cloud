#!/usr/bin/env python2

from distutils.core import setup
from distutils.extension import Extension

setup(
    name='chinese_cloud',
    version='1.1',
    ext_modules=[Extension("chinese_cloud.query_integral_image",
                           ["chinese_cloud/query_integral_image.c"])],
    packages=['chinese_cloud'],
    package_data={'chinese_cloud': ['stopwords', 'DroidSansFallbackFull.ttf']}
)
