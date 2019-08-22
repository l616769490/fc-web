#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: lijin
# Mail: lijin@dingtalk.com
# Created Time:  2019-07-17
#############################################


from setuptools import setup, find_packages		# 没有这个库的可以通过pip install setuptools导入

setup(
    name = "fcweb",												    # pip项目名
    version = "0.2.2",													# 版本号
    keywords = ("pip", "pathtool","timetool", "magetool", "mage"),							
    description = "阿里云函数计算web框架",									# 描述
    long_description = "贵州旅游大数据项目所用到的阿里云函数计算web框架",
    license = "MIT Licence",

    url = "https://github.com/l616769490/fc-web",				# 项目url
    author = "lijin",
    author_email = "lijin@dingtalk.com",

    packages = find_packages(),											# 导入目录下的所有__init__.py包
    include_package_data = True,
    platforms = "any",
    install_requires = ['fcutils']												# 项目引用的第三方包
)