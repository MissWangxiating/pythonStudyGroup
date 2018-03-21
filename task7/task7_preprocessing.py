#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/3/9  16:31
'''
将文本文件分句分词合并，得到训练集和测试集
'''
import codecs
import jieba
import os
import random
#将原始的txt文本语料处理成训练语料和测试语料，以9：1的比例来弄
#分句
def cut_sentence(file_path):
    with codecs.open(file_path,"r",encoding="utf-8") as f:
        #s = f.readlines() #这个函数只是按行读取，并没有分句的功能
        #因为原始语料txt不是无BOM的utf-8,文本开头会有非法字符\ufeff,阻碍对文本首末的空格清除，故需要替换掉
        s = f.read().replace("\ufeff","").strip()
        token=".!?。！？"
        line=[]
        lines_list=[]
        for word in s:
            if word in token:
                line.append(word)
                lines_list.append("".join(line).strip())
                line=[]
            else:
                line.append(word)
    return lines_list

#分词
def cut_words(line):
    words_list = jieba.cut(line,cut_all=False)#采用结巴分词的精确模式
    words = "/".join(words_list)
    return words

#遍历文件夹
def fun_folder(path):
    file_array=[]
    for root,dirs,files in os.walk(path):
        for file in files:
            file_path = str(root+"\\"+file)
            file_array.append(file_path)
    return file_array

#输出文本,一句话一句话的输出
def out_file(path,line):
    with codecs.open(path,"a",encoding="utf-8") as f:
        f.write(line+"\r\n")

def main():
    #遍历文件夹，读取待分句分词文件
    folder_path = r"分词文本"
    file_array = fun_folder(folder_path)
    words_list =[]
    for file_path in file_array:
        #分句
        lines_list = cut_sentence(file_path)
        for line in lines_list:
            words = cut_words(line)
            words_list.append(words)
    #将分词分句后的结果随机打乱
    random.shuffle(words_list)
    for i in range(len(words_list)):
        if i < 0.1*len(words_list):
            out_path1=r"test.txt"
            out_file(out_path1,words_list[i])
        else:
            out_path2=r"train.txt"
            out_file(out_path2,words_list[i])
    print("well done!")

if __name__ == '__main__':
    main()


