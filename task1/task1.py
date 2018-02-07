#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/2/7  9:22

#task1 读取文件和读入文件
import codecs
#读取文件
def readfile(path):
    with codecs.open(path,"r",encoding="utf-8") as f:
        lines = f.readlines()
    return "\n".join(lines)

#读入文件
def writefile(path,content):
    with codecs.open(path,"a",encoding="utf-8") as f:
        f.write(content)
        print("文件成功读入！")

def main():
    file_path ="task1.txt"
    content = readfile(file_path)
    print(content)
    add_content ="\r\n好好学python,天天向上！"
    writefile(file_path,add_content)
    print("well done")

if __name__=="__main__":
    main()




