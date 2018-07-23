#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
工具类
"""
import socket
import traceback

__author__ = 'foxiyang@qq.com'


def get_host_ip():
    """获取本机IP"""
    ip = '0.0.0.0'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        traceback.print_exc()
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    print(get_host_ip())
