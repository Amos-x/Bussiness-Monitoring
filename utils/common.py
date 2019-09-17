# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019/1/16 5:14 PM
#   FileName = common

import os
import subprocess
import re
import datetime


# 本地运行shell命令
def exec_shell(command):
    response = subprocess.run(command, shell=True, universal_newlines=True)
    response.check_returncode()


# 获取执行命令结果
def get_shell_response(command):
    return subprocess.check_output(command, shell=True, universal_newlines=True)


# 操作文件
class FileModify(object):
    def __init__(self,file_path, autocreate=False):
        self.file_path = file_path
        self._autocreate = autocreate
        self.check_exists()

    # 检查文件是否存在，不存在则报错或自动创建文件
    def check_exists(self):
        if not os.path.exists(self.file_path):
            if not self._autocreate:
                raise ValueError('文件不存在，请检查路径')
            else:
                with open(self.file_path,'w', encoding='utf-8') as f:
                    pass

    # 添加到文件末尾
    def add(self,context):
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(context+'\n')

    # 修改替换文件内容，old支持正则匹配
    def replace(self, old, new, line_num=None):
        with open(self.file_path, 'r+', encoding='utf-8') as f:
            ff = f.readlines()
            if line_num:
                ff[line_num] = re.sub(old, new, ff[line_num])
            else:
                for line in range(len(ff)):
                    ff[line] = re.sub(old, new, ff[line])

        with open(self.file_path,'w',encoding='utf-8') as f2:
            f2.writelines(ff)

    # 修改替换文件内容，支持正则匹配，按全文内容进行匹配
    def replace_all(self, old, new):
        content = self.content()
        content = re.sub(old, new, content, flags=re.S)
        self.cover(content)

    # 重写覆盖整个文件
    def cover(self,context):
        with open(self.file_path,'w', encoding='utf-8') as f:
            f.write(context)

    # 获取文件内容
    def content(self):
        with open(self.file_path,'r', encoding='utf-8') as f:
            return f.read()


def get_time_difference(timestamp):
    return datetime.datetime.fromtimestamp(timestamp) - datetime.datetime.fromtimestamp(0)
