#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志记录，基于basicConfig
"""
import logging
import os
from logging.handlers import TimedRotatingFileHandler, MemoryHandler

__author__ = 'foxiyang@qq.com'


class MyHandler(MemoryHandler):
    def emit(self, record):
        print(record.asctime + ' : ' + record.message)  # 可保存到数据库（暂未实现）
        super().emit(record)


def get_logger(name):
    log_format = '%(asctime)s - %(levelname)s - %(message)s - %(pathname)s'
    # 基础root配置,默认输出到控制台
    logging.basicConfig(format=log_format, level=logging.DEBUG)
    # 配置个性化logger
    formatter = logging.Formatter(log_format)
    logger = logging.getLogger(name)
    # 输出info日志到文件
    log_file = '{}/logs/{}.log'.format(os.path.dirname(os.path.dirname(__file__)), name)
    file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=10, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # 输出error信息到内存，然后保存到数据库
    memory_handler = MyHandler(102400)
    memory_handler.setLevel(logging.ERROR)
    memory_handler.setFormatter(formatter)
    logger.addHandler(memory_handler)

    return logger


if __name__ == '__main__':
    logger = get_logger('test')
    logger.info('Startup...Read app properties')
    logger = get_logger('test2')
    logger.info('Startup...Read app properties2')
