#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/2/27  19:17

#最大逆向匹配分词/ 每个txt文档统计词频
import xlrd
import codecs
import os
import shutil

#读取excel文档
def readxls(path):
    excel = xlrd.open_workbook(path)
    sheet = excel.sheets()[0]
    words = list(sheet.col_values(1))[1:]
    return words

#读取txt文本,返回句子列表
def readtxt(path):
    with codecs.open(path,"r",encoding="utf-8") as f:
        s = f.read()
    #对文本分句，存储为list
    cut_list = ".,?。，？"
    def Findtoken(cut_list,char):
        if char in cut_list:
            return True
        else:
            return False

    def cut(cut_list,lines):
        line = []
        l=[]
        for word in lines:
            if Findtoken(cut_list,word):
                line.append(word)
                l.append("".join(line))
                line=[]
            else:
                line.append(word)
        return l

    lines_list = cut(cut_list,s)
    return lines_list

#最大逆向匹配分词
def cut_word(sentences_list,word_dic,stop_word):
    word_cut = []
    #最大词长数为词典中最长的词数
    max_length = max(len(word) for word in word_dic)
    for sentence in sentences_list:
        sentence=sentence.strip()
        # 单句中的字个数
        n = len(sentence)
        word_cut_list=[]
        # 由于数组下标是由0开始，所以n值减一
        n = n - 1
        # 当句子没有切分完
        while n >= 0:
            matched = False
            for i in range(max_length, 0, -1):
                if sentence[n-i:n] in word_dic:
                    matched = True
                    if sentence[n-i:n] in stop_word:
                        n=n-i
                        break
                    else:
                        word_cut_list.append(sentence[n-i:n])
                        n=n-i
                        break
                if sentence[n-i:n] in stop_word:
                    matched = True
                    n = n-i
                    break
            if not matched:
                word_cut_list.append(sentence[n])
                n=n-i
        word_cut_list.reverse()
        words = "/".join(word_cut_list)
        word_cut.append(words)
    cut_content ="".join(word_cut)
    return cut_content

#创建保存分词结果的文件夹
def buildfolder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)
    return path

#遍历文件夹
def fun(folderpath):
    fileArray=[]
    for root,dirs,files in os.walk(folderpath):
        for fn in files:
            eachpath = str(root + "\\" +fn)
            fileArray.append(eachpath)
    return fileArray

#输出分词后的文本
def out_file(file_content,out_path):
    with codecs.open(out_path,"w",encoding="utf-8") as f:
        f.write(file_content)
    print("well done!")

def main():
    #创建分词结果文件夹
    save_folder_path = r"分词结果"
    folder_path = buildfolder(save_folder_path)
    print("新文件夹创建成功！")
    #获取所有待分词文本
    rawfile_path = r"分词文本"
    files_path = fun(rawfile_path)
    #获取分词词典
    words_dic_path = r"词表\words.xlsx"
    words_dic = readxls(words_dic_path)
    #获取停用词词典
    stop_words_path = r"词表\stopwords.xlsx"
    stop_words = readxls(stop_words_path)

    for path in files_path:
        rawfile = readtxt(path)
        cut_words = cut_word(rawfile,words_dic,stop_words)
        outfile_path = path.split("\\")[1]
        out_path = r"%s\%s_cut.txt"%(folder_path,outfile_path)
        out_file(cut_words,out_path)

if __name__ == '__main__':
    main()







