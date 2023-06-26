# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         test
# Description:  
# Author:       Rudy
# U:            project
# Date:         2020-03-25
#-------------------------------------------------------------------------------

"""
好好学习，天天向上。 
Mark:project
"""

# coding:utf-8
import os
from distutils.core import setup
from Cython.Build import cythonize
import shutil
# filter=[".py",".so",'.c'] linux的过滤条件
filter=[".py",".pyd",'.c'] #设置过滤后的文件类型 当然可以设置多个类型

def all_path(dirname):
    result = []  # 所有的文件
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            ext = os.path.splitext(apath)[1]  # 获取文件后缀 [0]获取的是除了文件名以外的内容
            # 筛选出.py 和 不是__init__的文件
            if ext in filter and os.path.splitext(filename)[0] not in('__init__','manage','test'):
                result.append(apath)
            else:
                pass
    return result

def rename(list):
    for i in list:
        if i.__contains__(".pyd"):
            re_name = i.split(".")[0] + '.pyd' #（linux的是.so文件）
            print(i.split('.'))
            os.rename(i, re_name)
        elif i.__contains__(".c"):
            os.remove(i)

if __name__ == '__main__':
    path = os.getcwd()
    list = all_path(path)
    print(list)
    print(len(list))
    rename(list)

    
    
    
    
    
"""
好好学习，天天向上。 
project
"""