# -*- coding: utf-8 -*-
#python 27
#xiaodeng
#python之模块py_compile用法(将py文件转换为pyc文件)；二进制文件，是由py文件经过编译后，生成的文件.
 
#办法一：
import py_compile
#加r前缀进行转义
py_compile.compile(r'C:\Users\zy\gitspace\tkinter-huffman\zyheap.py')#py文件完整的路径.
 
 
# 办法二：
#cmd命令符下操作步骤
# 1、打开cmd，切换到 cd c:\\python34
# 2、运行
#      1）python -m py_compile D:\test.py   #跟随完整路径
#      2）python -m py_compile /root/src/{file1,file2}.py   #这是同时转换多个文件
# 3、会在需转译文件的目录下生成一个“__pycache__”目录/test.cpython-34.pyc文件
 
#-m 相当于脚本中的import，这里的-m py_compile 相当于上面的 import py_compile