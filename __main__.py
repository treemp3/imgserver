#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
文件上传下载接口
"""
import datetime
import os
import random
import time

from bottle import Bottle, request, run, response, static_file, abort

from libs.config import conf_global
from libs.log import get_logger
from libs.utils import get_host_ip

__author__ = 'foxiyang@qq.com'

current_dir = conf_global.get('app', 'current_dir', fallback='storage_0')  # 获取当前存放文件的目录别名
logger = get_logger(__name__)
app = Bottle()


@app.route('/upload/<file_type>', method='POST')
def do_upload(file_type):
    """上传文件接收并保存"""
    if 'multipart/form-data' not in request.headers.get('Content-Type'):
        return {'code': 2, 'msg': 'Content-Type must be multipart/form-data!'}
    if not request.files:
        return {'code': 1, 'msg': 'Parameter file must not be empty!'}
    if file_type not in ('permanent', 'temporary'):
        return {'code': 1, 'msg': 'Parameter file_type must not be empty!'}

    # 处理文件上传路径
    now = datetime.datetime.now()
    home_path = conf_global.get('app', current_dir, fallback='/home/files/')  # 获取当前存放文件的主目录路径
    file_path = file_type + now.strftime('/%Y/%m/%d/')  # 定义存放文件的相对路径
    full_path = home_path + file_path
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    # 定义返回数据，将处理结果存入form字典后返回客户端
    form = {'code': 0, 'msg': 'OK'}
    # 处理表单内多个文件域的情况
    for item in request.files:
        # 取得一个文件域的所有上传文件
        upload_list = request.files.getall(item)

        for upload in upload_list:
            logger.info('IP：%s，文件域：%s，文件名：%s', request.remote_addr, upload.name, upload.raw_filename)

            # 定义新文件名
            old_name, ext = os.path.splitext(upload.raw_filename)
            file_suffix = str(('.png', '.jpg', '.jpeg'))
            file_suffix = eval(conf_global.get('app', 'file_suffix', fallback=file_suffix))
            if ext not in file_suffix:
                return {'code': 3, 'msg': 'File extension not allowed.'}
            file_name = str(int(time.time() * 1000)) + str(random.randint(100, 999)) + ext
            upload.filename = file_name

            # 定义下载路径URL，默认使用当前URL前缀构造，可将down_prefix加入配置文件，以便个性化下载路径
            this_prefix = request.urlparts[0] + '://' + request.urlparts[1] + '/'  # 示例：http://192.168.0.1:8080/
            down_prefix = conf_global.get('app', 'down_prefix', fallback=this_prefix)
            file_url = down_prefix + get_host_ip() + '/' + current_dir + '/' + file_path + file_name

            form_field = upload.name  # 上传文件域
            if form_field.endswith('[]'):
                # 如果在一个文件域上传多个文件，需使用h5 input标签的multiple属性
                # 并且在name属性后增加[]字符串，表示该文件域上传的是多文件
                form_field = form_field.replace('[]', '')
                # 保存为图片列表
                if form_field not in form:
                    form[form_field] = [file_url]
                else:
                    form[form_field].append(file_url)
            else:
                # 保存为单个图片
                form[form_field] = file_url

            logger.info('文件存储路径：%s', full_path)
            upload.save(full_path, True)  # appends upload.filename automatically
    return form


@app.route('/<ip:re:\d+\.\d+\.\d+\.\d+>/<path_alias>/<filename:path>', method='GET')
def server_static(ip, path_alias, filename):
    home_path = conf_global.get('app', path_alias, fallback='/home/files/')  # 获取当前存放文件的主目录路径
    return static_file(filename, root=home_path)


@app.route('/<ip:re:\d+\.\d+\.\d+\.\d+>/<path_alias>/<filename:path>', method='DELETE')
def server_static(ip, path_alias, filename):
    home_path = conf_global.get('app', path_alias, fallback='/home/files/')  # 获取当前存放文件的主目录路径
    file_path = home_path + filename

    logger.info('删除图片：' + file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {'code': 0, 'msg': 'OK'}
    else:
        return {'code': -1, 'msg': 'File does not exist.'}


@app.hook('before_request')
def permission():
    """请求鉴权，预留，暂未实现"""
    token = request.headers.get('token', 'unknown_token')
    logger.info('请求Token：' + token)
    if token != '123456':
        pass  # abort(403, 'Access denied.')


@app.hook('after_request')
def enable_cors():
    origin = request.headers.get('Origin', '*')
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8001, debug=True)
