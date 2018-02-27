#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/2/22  18:13

#将Excel格式的文件转化为TXT,每10条数据存入一个txt中，
# 每个txt中每条数据用分割线分割，且每个txt用1、2、3...序号命名
import xlrd
import codecs
import os
import shutil
#读取Excel文件
def readxls(path):
    excel = xlrd.open_workbook(path)
    sheet = excel.sheets()[0]
    data = []
    #nrows按行读取excel文件，每行数据作为一个list存储进入data这个list中
    for i in range(sheet.nrows):
        data.append(list(sheet.row_values(i)))
    return data

#创建文件夹
def build_folder(folderpath):
    if os.path.exists(folderpath):
        shutil.rmtree(folderpath)#若存在则删去已存在的文件夹名
        os.makedirs(folderpath)
    else:
        os.makedirs(folderpath)
    #返回创建的文件夹路径
    return folderpath

#读取10条数据存入txt中,函数输入值fpath 是指文件夹路径
def new_txt(fpath,data_list):
    #获取数据标题栏
    title = data_list[0]
    #读入数据
    i=0
    for item in data_list[1:]:
        n = i//10 + 1
        #输入路径时要考虑\转义字符，另外路径中的划分符是否操作系统不一样偏向不一样
        with codecs.open("%s\\%d.txt"%(fpath,n),"a",encoding="utf-8") as f:
            for j in range(len(title)):
                f.write("【%s】%s"%(title[j],item[j])+"\r\n")
            f.write("-----------------------\r\n")
        i=i+1

    print("well done!")

#主函数
def main():
    #创建文件夹
    folder_path = r"task3_数据格式转换"
    build_folder(folder_path)
    #读取数据
    file_path =r"材料1.xlsx"
    data_list = readxls(file_path)
    #将数据存储到txt文件中
    new_txt(folder_path,data_list)

if __name__ == '__main__':
    main()









