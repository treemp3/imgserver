#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
读取全局配置文件
"""
import configparser

import os

__author__ = 'foxiyang@qq.com'

conf_global = configparser.ConfigParser()
conf_global.read(os.path.dirname(os.path.dirname(__file__)) + '/conf/app.conf', encoding='utf-8')


if __name__ == '__main__':
    print(conf_global['card3500']['db_pass'])
