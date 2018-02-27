#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/2/22  17:30

#将期刊论文作者合并
import xlrd
import codecs

#读取excel文件
def readxls(path):
    excel = xlrd.open_workbook(path)
    sheet = excel.sheets()[0]
    data=[]
    for i in range(1,sheet.nrows):
        data.append(list(sheet.row_values(i)))
    return data

#合并论文作者
def pull_author(rows_list):
    author_dic={}
    for row in rows_list:
        paper_id = row[0]
        paper_name = row[1]
        paper_author = row[2]
        paper_key = paper_id + "\t" + paper_name

        if paper_key in author_dic.keys():
            author_dic[paper_key] = author_dic[paper_key] +";" +paper_author
        else:
            author_dic[paper_key] = paper_author
    return author_dic

#写入txt文件
def out_file(content,path):
    with codecs.open(path,"w",encoding="utf-8") as f:
        f.write(str(content))
    print("存储成功")

def main():
    #读取Excel文件
    excel_path = r"材料2.xlsx"
    rows_list = readxls(excel_path)
    #print(rows_list[1])
    #合并论文作者
    author_dic = pull_author(rows_list)
    #print(len(author_dic))
    #输出结果到txt文件
    #利用列表生成将字典格式的数据转化为列表形式的数据
    L = [k+"\t"+ v for k,v in author_dic.items()]
    content = "\r\n".join(L)
    #print(len(L))
    out_path = r"数据合并.txt"
    out_file(content,out_path)
    print("well done!")

if __name__ =="__main__":
    main()
