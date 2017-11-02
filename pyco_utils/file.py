# -*- coding: utf-8 -*-
import os


def ensure_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def command(cmd):
    status = os.system(cmd)
    code = os.WEXITSTATUS(status)
    return code == 0


def list_file_with_prefix(prefix, path='.'):
    files = []
    for f in os.listdir(path):
        if f.startswith(prefix):
            files.append(f)
    return files


def resize_image(image='', w=64, h=64):
    name, ext = image.rsplit('.', 1)
    t = '{}_{}x{}.{}'.format(name, w, h, ext)
    cmd = 'magick {} -resize 64x64 {}'.format(image, t)
    return command(cmd)


def zipfile(filename, path='.', zipname=''):
    # brew install p7zip
    # 7z a -v1G baidu_search.zip baidu_search
    # 压缩文件上传
    if zipname == '':
        zipname = '{filename}.zip'.format(filename=filename)
    cmd = '7z a -v500m {} {}/{}'.format(zipname, path, filename)
    return command(cmd)


def proxy_wget_file(url, file='temp.html'):
    # command = 'proxychains4 wget www.google.com'
    cmd = 'proxychains4 wget -O "{file}" "{url}"'.format(file=file, url=url)
    if command(cmd):
        with open(file, 'r+') as f:
            return f.read()
