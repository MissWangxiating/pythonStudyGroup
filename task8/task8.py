#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/3/15  9:53

'''
评价CRF++学习的结果，即计算测试语料结果中的P(精确率)，R(召回率)，F值
精确率=识别正确的个数/机器识别的个数
召回率=识别正确的个数/人工标注的个数
F值=（2*准确率*召回率）/（准确率+召回率）
'''
'''
在本语料中可以视为分别计算B,E,ME,M的精确率，召回率，F值
'''
import codecs
#读取机器学习测试结果，将每一行转化为包含三个元素的list
def readtxt(path):
    with codecs.open(path,"r",encoding="utf-8") as f:
        new_line=[]
        s=f.readlines()
        for line in s:
            line=line.strip()
            if len(line)>=3:
                line_list = line.split("\t")
                new_line.append(line_list)
        return new_line

#计算sign精确率
def count_precision(line_list,sign):
    b1=0
    b2=0
    for line in line_list:
        #print(line[1])
        if line[1]==sign:
            b2 = b2+1
           # print(b2)
            if line[2]==sign:
                b1 = b1+1
    precision = b1/b2
    #print(precision)
    return precision

#计算sign召回率
def count_recall(line_list,sign):
    b1=0
    b2=0
    for line in line_list:
        if line[2]==sign:
            b2 = b2+1
            if line[1]==sign:
                b1 = b1+1
    recall = b1/b2
    return recall
#计算F值
def count_F(p,r):
    F = (2*p*r)/(p+r)
    return F
#将结果输出到txt文本中
def out_file(content,path):
    with codecs.open(path,"a",encoding="utf-8") as f:
        f.write(content)

def main():
    #读入机器学习结果文本
    file_path = r"output.txt"
    line_list = readtxt(file_path)
    #计算B,BE,M,E 的准确率
    B_precision = count_precision(line_list,"B")
    BE_precision = count_precision(line_list,"BE")
    M_precision = count_precision(line_list,"M")
    E_precision = count_precision(line_list,"E")
    #计算B,M,E,BE的召回率
    B_recall = count_recall(line_list,"B")
    M_recall = count_recall(line_list,"M")
    E_recall = count_recall(line_list,"E")
    BE_recall = count_recall(line_list,"BE")
    #计算B,M,E,BE的F值
    B_F = count_F(B_precision,B_recall)
    M_F = count_F(M_precision,M_recall)
    E_F = count_F(E_precision,E_recall)
    BE_F = count_F(BE_precision,BE_recall)
    #输出结果到txt文档
    content1 = "B的精确率为%s,召回率为%s,F值为%s。\r\n"%(str(B_precision),str(B_recall),str(B_F))
    content2 = "M的精确率为%s,召回率为%s,F值为%s。\r\n"%(str(M_precision),str(M_recall),str(M_F))
    content3 = "E的精确率为%s,召回率为%s,F值为%s。\r\n"%(str(E_precision),str(E_recall),str(E_F))
    content4 = "BE的精确率为%s,召回率为%s,F值为%s。\r\n"%(str(BE_precision),str(BE_recall),str(BE_F))
    content = content1+content2+content3+content4
    out_path = r"result.txt"
    out_file(content,out_path)
    print("well done!")

if __name__ == '__main__':
    main()