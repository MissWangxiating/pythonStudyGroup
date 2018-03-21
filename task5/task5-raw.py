#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/3/1  16:21

import xlrd
import codecs
import os
import shutil

#读取分词字典
def word_dic(dicfile_path):
    excel = xlrd.open_workbook(dicfile_path)
    sheet = excel.sheets()[0]
    #读取第二列的数据
    data_list=list(sheet.col_values(1))[1:]
    return data_list

#读取停用词表
def stop_words(stopfile_path):
    excel = xlrd.open_workbook(stopfile_path)
    sheet = excel.sheets()[0]
    #读取第二列的数据
    data_list=list(sheet.col_values(1)[1:])
    return data_list

#读取待分词文本
def file_read(rawfile_path):
    with codecs.open(rawfile_path,"r",encoding="utf8") as f:
        s = f.read()
        #对文本进行分句，生成list
        #设置分句的标志符号，英文的三个，中文的三个
        cutlist=".?! 。？！"
        #检查某字符是否是分句标志符号，如果是，返回true,否则返回false
        def Findtoken(cutlist,char):
            if char in cutlist:
                return True
            else:
                return False

        def cut(cutlist,lines):
            l=[]
            line=[]
            for i in lines:
                if Findtoken(cutlist,i):
                    line.append(i)
                    l.append(''.join(line))
                    line=[]
                else:
                    line.append(i)
            return l
        #参照网上代码进行分句，但是还是不是很明白
        sentences=cut(list(cutlist),s)
        sentences_list=[]
        for line in sentences:
            if line.strip()!="":
                li=line.strip().split()
                sentences_list.append(li[0])
                '''
                for sentence in li:
                    print(type(sentence))
                    print(sentence)
                '''
    return sentences_list
#逆向最大匹配分词算法,
# 输入为list格式的一篇文本，list元素为单句话
# 输入为分词词典，停用词词典
# 输出为分词后的加了/的字符串
def cut_words(raw_sentences,words_list,stop_list):
    words_cut=[]
    # 最大词长数，为分词词典中的最长词长
    max_length = max(len(word) for word in words_list)
    #print(max_length)

    for sentence in raw_sentences:
        sentence=sentence.strip()
        #单句中的词数n
        n= len(sentence)
        words_cut_list=[]
        #因为list下标是从0开始，所以单句中最后一个字的下标应为n-1
        n=n-1
        #该条件表示单句中仍有词需要切分时
        while n>=0:
            matched=False
            #根据最大词长，依次递减切分词
            for i in range(max_length,0,-1):
                s=sentence[n-i:n]
                if s in words_list:
                    matched = True
                    #如果词同时在词典和停用词表中，直接略去，否则添加入分词列表
                    if s in stop_list:
                        n=n-i
                        break
                    else:
                        words_cut_list.append(s)
                        n=n-i
                        break
                #如果词在停用词表中，直接略去
                if s in stop_list:
                    matched=True
                    n=n-i
                    break
            #如果分到最后都没有在任何词表中南，直接添加进分词列表中
            if not matched:
                words_cut_list.append(sentence[n])
                n=n-i
        #单句切分的结果，为words_cut_list,表中的元素都是顺序都是反的
       # print("qiefenjieguo",type(words_cut_list))
        #把结果中元素倒序输出
        # reverse()函数直接在list本身操作就好，不需要再把它转置的列表赋值给新的变量
        #否则会出现得到的变量为Nonetype
        words_cut_list.reverse()
        words="/".join(words_cut_list)
        words_cut.append(words)
    cut_content="".join(words_cut)
    return cut_content

#创建保存分词结果的文件夹
def buildfolder(echkeyfile):
    if os.path.exists(echkeyfile):
        shutil.rmtree(echkeyfile)
        os.makedirs(echkeyfile)
    else:
        os.makedirs(echkeyfile)
    return echkeyfile

#遍历文件夹
def fun(folderpath):
    fileArray=[]
    for root,dirs,files in os.walk(folderpath):
        for fn in files:
            eachpath = str(root + "\\" + fn)
            fileArray.append(eachpath)
    return fileArray


#输出分词后的文本
def out_file(file_content,out_path):
    with codecs.open(out_path,"w",encoding="utf8") as f:
        f.write(file_content)
    print("well done")


def main():
    #创建分词结果存储文件夹
    save_folder_path=r"分词结果"
    folderpath=buildfolder(save_folder_path)
    print(folderpath)
    #获得所有分词文本
    rawfiles_path = r"分词文本"
    filespath = fun(rawfiles_path)
    '''
    for path in filepath:
        print(path)
    '''
    for path in filespath:
        # 分词文本
        file_path = path
        rawfile = file_read(file_path)
        # 分词词典
        wordfile_path = r"词表\words.xlsx"
        words_dic = word_dic(wordfile_path)
        # 停用词词典
        stopfile_path = r"词表\stopwords.xlsx"
        stopwords = stop_words(stopfile_path)
        # 分词
        content_cut = cut_words(rawfile, words_dic, stopwords)
        #print(content_cut)
        # 输出文本
        outfile_path=path.split("\\")[1]
        out_path = r"%s\%s_cut.txt"%(folderpath,outfile_path)
        out_file(content_cut, out_path)

if __name__=="__main__":
    main()