from distutils.core import setup
from distutils.extension import Extension

setup(
    name='chinese_cloud',
    ext_modules=[Extension("chinese_cloud.query_integral_image",
                           ["chinese_cloud/query_integral_image.c"])],
    packages=['chinese_cloud']
)
