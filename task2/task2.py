#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/2/13  11:51

#子任务1：统计词频；子任务2：合并数据
import xlrd
#读取excel文件的第i列，i=0,1,2,3......
def readxls(path,i):
    xl = xlrd.open_workbook(path)
    sheet = xl.sheets()[0] #表示读取第一个工作表sheet
    data = list(sheet.col_values(i))
    data_list = data[1:]
    return data_list
#统计频次
def fluency(word_list):
    word_dic={}
    fluency_list =[]
    for word in word_list:
        if word in word_dic.:
            word_dic[word] += 1
        else:
            word_dic[word] = 1
    for key in word_dic:
        fluency_list.append("%s \t %s" %(key,word_dic[key]))
    return fluency_list

#输出词频列表
def out_fluencytxt(words_fluency_list):
    path=input("please input the file path you want to save:\n")
    with open(path,"w",encoding="utf-8") as f:
        for words_fluency in words_fluency_list:
            f.write(words_fluency+"\n")
    print("词频txt文件存储成功！")

#统计期刊词频
def paper_count():
    #读取Excel文件D列期刊名
    xls_path =r"材料1.xlsx"
    paper_list = readxls(xls_path,3)
    # 统计期刊名频次
    paper_fluency = fluency(paper_list)
    #输出统计结果
    print("---输出期刊名词频列表---")
    out_fluencytxt(paper_fluency)
    print("期刊频次统计完成完成！")

#统计关键词词频
def keywords_count():
    #读取Excel文件C列关键词
    xls_path = r"材料1.xlsx"
    keywords_list = readxls(xls_path,2)
    #将每组关键词处理成单个关键词
    keyword_list=[]
    for keywords in keywords_list:
        words_list = keywords.split("/")
        for word in words_list:
            keyword_list.append(word)
    #统计关键词频次
    words_fluency = fluency(keyword_list)
    #输出统计结果
    print("---输出关键词词频列表---")
    out_fluencytxt(words_fluency)
    print("关键词频次统计完成!")
def main():
    #统计期刊名词频
    paper_count()
    #统计关键词词频
    keywords_count()
    print("well done!")

if __name__ == "__main__":
    main()




