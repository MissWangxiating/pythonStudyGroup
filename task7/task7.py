#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/3/12  20:36
'''
 将训练集和测试集处理成crf++能够处理的数据格式
'''
import codecs
#读取文件
def readfile(txt_path):
    with codecs.open(txt_path,"r",encoding="utf-8") as f:
        s=f.readlines()
    return s
#添加标记
def addtag(line):
    word_list=line.split("/")
    word_tag_list=[]
    for word in word_list:
        word = word.strip()
        s = list(word)
        if len(s)>=3:
            s[0]=s[0]+"\t"+"B"
            s[-1]=s[-1]+"\t"+"E"
            for i in range(1,len(word)-1,1):
                s[i] = s[i]+"\t"+"M"
        elif len(s)==2:
            s[0]=s[0]+"\t"+"B"
            s[-1]=s[-1]+"\t"+"E"
        elif len(s)==1:
            s[0]=s[0]+"\t"+"BE"
        words = "\r\n".join(s)
        word_tag_list.append(words)
    word_tag_list.append(" ") #在句末加空格
    return word_tag_list

#输出文件
def out_file(text_path,word_tag_list):
    with codecs.open(text_path,"a",encoding="utf-8") as f:
        for word_tag in word_tag_list:
            f.write(word_tag+"\r\n")

def work(in_path,out_path):
    lines_list = readfile(in_path)
    for line in lines_list:
        word_tag_list = addtag(line)
        out_file(out_path,word_tag_list)
    print("well done!")

def main():
    # 读取训练集
    train_path = r"train.txt"
    out_train_path = r"out_train.txt"
    test_path = r"test.txt"
    out_test_path=r"out_test.txt"
    work(train_path,out_train_path)
    work(test_path,out_test_path)

if __name__ == '__main__':
    main()



