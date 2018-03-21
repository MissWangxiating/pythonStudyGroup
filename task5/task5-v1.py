#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/3/1  15:50

import codecs
import xlrd
import os
import shutil

#读取txt文本,返回句子列表
def readtxt(path):
    with codecs.open(path,"r",encoding="utf-8") as f:
        s = f.read()
    #对文本分句，存储为list
    cut_list = ".?!。？！"
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

#读取excel文档
def readxls(path):
    excel = xlrd.open_workbook(path)
    sheet = excel.sheets()[0]
    words = list(sheet.col_values(1))[1:]
    return words

#最大逆向匹配分词
def cut_word(sentences,word_dic,stopwords):
    word_cut = []
    #最大词长数为词典中最长的词数
    max_length = max(len(word) for word in word_dic)
    print(max_length)
    for sentence in sentences:
        # 去除文本两侧多余的空格
        sentence_new = sentence.strip()
        # 待切分句子中的单词个数
        words_length = len(sentence_new)
        #print(words_length)
        word_cut_list = []
        # 当句子没有切分完,n在一直减小，n的大小肯定会比max_length小的。
        while words_length > 0:
            max_len = min(max_length, words_length)
            for i in range(max_len, 0, -1):
                new_word = sentence_new[words_length - i:words_length]
                #去除停用词
                if new_word in stopwords:
                    words_length = words_length - i
                    break
                elif new_word in word_dic:
                    word_cut_list.append(new_word)
                    words_length = words_length - i
                    break
                elif i == 1:
                    word_cut_list.append(new_word)
                    words_length = words_length - 1
        word_cut_list.reverse()
        words = "/".join(word_cut_list)
        word_cut.append(words.lstrip("/"))
    return word_cut

#词频统计
def count(words_list):
    word_dic={}
    wordcount_list=[]
    for sentence in words_list:
        word_list = sentence.split("/")
        for word in word_list:
            if word in word_dic:
                word_dic[word] = word_dic[word] + 1
            else:
                word_dic[word] = 1
    for key,value in word_dic.items():
        wordcount_list.append("%s:%d"%(key,value))
    words_count = "\r\n".join(wordcount_list)
    return words_count

#输出分词文本
def outfile(out_path,sentences,words_count):
    with codecs.open(out_path,"a","utf-8") as f:
        for sentence in sentences:
            f.write(sentence)
        f.write("\r\n 本篇章的词频统计:\r\n")
        f.write(words_count)
    print("well done!")

#创建存储分词结果的文件夹
def buildfolder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    return path

#遍历文件夹
def funfolder(path):
    fileArray=[]
    #os.walk()函数
    for root,dirs,files in os.walk(path):
        for fn in files:
            everypath = str(root + "\\" + fn)
            fileArray.append(everypath)
    return fileArray

def main():
    #读取待分词文本
    files_path =r"分词文本"
    path_list = funfolder(files_path)
    #读取分词词典
    dic_path = r"词表/words.xlsx"
    words_dic = readxls(dic_path)
    #读取停用词词典
    stopwords_path = r"词表/stopwords.xlsx"
    stopwords = readxls(stopwords_path)
    #创建存储分词结果文件夹
    store_folder = r"分词结果"
    folder_path = buildfolder(store_folder)
    #分词
    for file in path_list:
        #读取待分词文本
        raw_file = readtxt(file)
        print(file)
        #最大逆向匹配分词，且统计词频
        content_cut = cut_word(raw_file,words_dic,stopwords)
        words_count = count(content_cut)
        #输出文本
        new_file = file.split("\\")[1]
        out_path = r"%s//%s_cut"%(folder_path,new_file)
        outfile(out_path,content_cut,words_count)
        print("well done!")

def main_test():
    #读取待分词文本
    rawfile_path = r"分词文本/1.txt"
    rawfile = readtxt(rawfile_path)
    #读取分词词典
    wordsdic_path = r"词表/words.xlsx"
    words_dic = readxls(wordsdic_path)
    #读取停用词典
    stopwords_path = r"词表/stopwords.xlsx"
    stop_words = readxls(stopwords_path)
    #逆向最大匹配分词
    content_cut = cut_word(rawfile,words_dic,stop_words)
    words_count = count(content_cut)
    #输出文本
    outfile_path = r"分词结果.txt"
    outfile(outfile_path,content_cut,words_count)

if __name__ == '__main__':
    main()

