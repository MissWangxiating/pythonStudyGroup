#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/3/9  10:06

'''
 对数据进行预处理，调用jieba进行分词
'''
import codecs
import xlrd
import jieba
import os
import shutil
import re
#读取文件
def readtxt(path):
    with codecs.open(path,"r",encoding="utf-8") as f:
        content = f.read()
    return content

#读取excel文件
def readxls(path):
    excel = xlrd.open_workbook(path)
    sheet = excel.sheets()[0]
    words = list(sheet.col_values(1))[1:]
    return words

#调用结巴分词
def cutwords(content,stopwords):
    word_cut =[]
    #content = content.strip()
    re.sub('\s',"",content)
    content.replace(" ","").replace("\r\n","")
    #采用精确模式分词
    seg_list = jieba.cut(content,cut_all=False)
    for word in seg_list:
        if word not in stopwords:
            word_cut.append(word)
    #print(word_cut[0])
    words_cut = "/".join(word_cut)
    return words_cut

#写入文件
def writefile(path,content):
    with codecs.open(path,"w",encoding="utf-8") as f:
        f.write(content)
        print("well done!")
#创建存储分词结果文件夹
def buildfolder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    return path
#遍历文件夹
def funfolder(path):
    fileArray = []
    for root,dirs,files in os.walk(path):
        for file in files:
            each_path = str(root + "//" + file)
            fileArray.append(each_path)
    return fileArray

def main():
    #创建存储分词结果文件夹
    folder_path = r"分词结果"
    buildfolder(folder_path)
    print("分词结果文件夹创建成功！")
    #读取停用词典
    stopwords_path = r"stopwords.xlsx"
    stop_words = readxls(stopwords_path)
    # 读取待分词文本
    files_folder = r"分词文本"
    files_list = funfolder(files_folder)
    for file_path in files_list:
        file = readtxt(file_path)
        # jieba分词
        words_cut = cutwords(file, stop_words)
        # 写入文件
        #print(file_path)
        file_name_list = file_path.split("//")
        file_name = file_name_list[1]
        out_path = "%s\\%s_cut.txt"%(folder_path,file_name)
        writefile(out_path, words_cut)
        print("well done!")



if __name__ == '__main__':
    main()




