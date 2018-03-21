#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/3/9  9:33

'''
计算文档的TF-IDF
'''
import codecs
import os
import math
import shutil

#读取文本文件
def readtxt(path):
    with codecs.open(path,"r",encoding="utf-8") as f:
        content = f.read().strip()
    return content

#统计词频
def count_word(content):
    word_dic ={}
    words_list = content.split("/")
    del_word = ["\r\n","/s"," ","/n"]
    for word in words_list:
        if word not in del_word:
            if word in word_dic:
                word_dic[word] = word_dic[word]+1
            else:
                word_dic[word] = 1
    return word_dic

#遍历文件夹
def funfolder(path):
    filesArray = []
    for root,dirs,files in os.walk(path):
        for file in files:
            each_file = str(root+"//"+file)
            filesArray.append(each_file)
    return filesArray


#计算TF-IDF
def count_tfidf(word_dic,words_dic,files_Array):
    word_idf={}
    word_tfidf = {}
    num_files = len(files_Array)
    for word in word_dic:
        for words in words_dic:
            if word in words:
                if word in word_idf:
                    word_idf[word] = word_idf[word] + 1
                else:
                    word_idf[word] = 1
    for key,value in word_dic.items():
        if key !=" ":
            word_tfidf[key] = value * math.log(num_files/(word_idf[key]+1))

    #降序排序
    values_list = sorted(word_tfidf.items(),key = lambda item:item[1],reverse=True)
    return values_list

#新建文件夹
def buildfolder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    print("成功创建文件夹！")

#写入文件
def out_file(path,content_list):
    with codecs.open(path,"a",encoding="utf-8") as f:
        for content in content_list:
            f.write(str(content[0]) + ":" + str(content[1])+"\r\n")
    print("well done!")

def main():
    #遍历文件夹
    folder_path = r"分词结果"
    files_array = funfolder(folder_path)
    #生成语料库
    files_dic = []
    for file_path in files_array:
        file = readtxt(file_path)
        word_dic = count_word(file)
        files_dic.append(word_dic)
    #新建文件夹
    new_folder = r"tfidf计算结果"
    buildfolder(new_folder)

    #计算tf-idf,并将结果存入txt
    i=0
    for file in files_dic:
        tf_idf = count_tfidf(file,files_dic,files_array)
        files_path = files_array[i].split("//")
        #print(files_path)
        outfile_name = files_path[1]
        #print(outfile_name)
        out_path = r"%s//%s_tfidf.txt"%(new_folder,outfile_name)
        out_file(out_path,tf_idf)
        i=i+1

if __name__ == '__main__':
    main()


