#!/usr/bin/env python
#-*- coding:utf-8 -*-
#@author: wangxiating
#@time :2018/2/23  21:29
#实现关键词共现矩阵
import xlrd
import codecs

#读取Excel文件中的关键词
def read_keywords(fpath):
    excel = xlrd.open_workbook(fpath)
    sheet = excel.sheets()[0] #第一个列表
    #读取关键词列
    keywords_list = list(sheet.col_values(2))[1:]
    words_list=[]
    #将一组关键词转换为list格式，words_list 为[[keyword_list1],[keyword_list2]...]
    for keywords in keywords_list:
        keyword_list = keywords.split("/")
        words_list.append(keyword_list)
    return words_list


#获取关键词词典
def keyword_dic(keywords_list):
    words_dic = []
    for keywords in keywords_list:
        for keyword in keywords:
            #去除可能存在的空格
            keyword = str(keyword).strip()
            if keyword not in words_dic:
                words_dic.append(keyword)
    return words_dic

#生成关键词共现矩阵
def comatrix(keywords,keywords_lines):
    n = len(keywords)
    #初始化共现矩阵
    matrix =[[0 for rows in range(n)] for cols in range(n)]
    for i in range(n):
        for j in range(n):
            if i==j:
                matrix[i][j]=0
            else:
                for line in keywords_lines:
                    if keywords[i] in line and keywords[j] in line:
                        matrix[i][j] +=1
    return matrix
#将关键词共现矩阵输出到txt文本中
def outfile(path,matrix,keywords):
    with codecs.open(path,"w",encoding="utf-8") as f:
        f.write(""+"\t")
        for word in keywords:
            f.write(word+"\t")
        f.write("\r\n")
        i=0
        for rows in matrix:
            rows_list = map(str, rows)
            rows_word = "\t".join(rows_list)
            #print(keywords[i])
            row = keywords[i]+"\t" + rows_word
            f.write(row+"\r\n")
            i=i+1
    print("共现矩阵存储完成！")



def main():
    filepath = r"材料1.xlsx"
    keywords_list = read_keywords(filepath)
    words_dic = keyword_dic(keywords_list)
    #print(len(words_dic))
    matrix = comatrix(words_dic, keywords_list)
    out_path = r"matrix.txt"
    outfile(out_path, matrix, words_dic)
    print("well done!")

if __name__ == '__main__':
    main()









