#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/3/1  15:50

import codecs
import xlrd

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
def cut_word(sentences,word_dic):
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
                if new_word in word_dic:
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

#去除停用词
def del_words(stop_words,words_cut):
    new_words_cut = []
    for words in words_cut:
        word_list = words.split("/")
        print(word_list)
        words_length = len(word_list)-1
        print(words_length)
        '''
        for word in word_list:
            print(word)
            if word in stop_words:
                #为什么去除停用词不能都去除,因为此函数是移除列表中某个值的第一个匹配项
                word_list.remove(word)
                #print(word)
                #print("delete a word")
            '''
        for i in range(words_length):
            if word_list[i] in stop_words:
                del word_list[i]
                print("del a word")
        new_words = "/".join(word_list)
        print(new_words)
        new_words_cut.append(new_words)
    return new_words_cut

#输出分词文本
def outfile(out_path,sentences):
    with codecs.open(out_path,"a","utf-8") as f:
        for sentence in sentences:
            f.write(sentence)
    print("well done!")

def main():
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
    content_cut = cut_word(rawfile,words_dic)
    #去除停用词
    final_content = del_words(stop_words,content_cut)
    #输出文本
    outfile_path = r"分词结果.txt"
    outfile(outfile_path,final_content)

if __name__ == '__main__':
    main()

