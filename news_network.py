# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 01:05:34 2023

@author: xwh
"""

import numpy as np
import pandas as pd
#import pickle
#循环读取文件夹中的所有pkl文件
import networkx as nx
import matplotlib.pyplot as plt
import os
path = r"G:\\12_Database\\股吧文本数据"
df = pd.DataFrame()
file_list = os.listdir(path)
for file in file_list:
    if file[-3:]=='pkl':
        with open(path+'\\'+file,'rb') as f:
            data = pickle.load(f)
    #重新设定data列名
    data.columns = ['序号','read','comment','year','date','day','title','user']
    userlist = data['user']
    #去除重复的用户
    userlist = list(set(userlist))
    #删除file最后四个字符
    filename = file[:-4]
    #保存为字典格式，key为file，value为userlist，字典名称为filename
    dictdata = {filename:userlist}
    #将dictguba重命名为filename变量的值
    exec(filename + '=dictdata')

#将file_list每个元素的后四个字符删除
file_name_list = [x[:-4] for x in file_list]


matrix = np.eye((len(file_name_list)))
for x in range(len(file_name_list)):
    #将字典中的value转化为list
    #按字典名称取出字典的值
    #将字典的值转化为list
    dict_name1 = eval(file_name_list[x])
    all_lists_1 = [list(value_) for value_ in dict_name.values()]
    all_lists_1 = all_lists_1[0]   
    for y in range (x+1, len(file_name_list)):
        dict_name2 = eval(file_name_list[y])
        all_lists_2 = [list(value_) for value_ in dict_name2.values()]  
        all_lists_2 = all_lists_2[0]
        if set(all_lists_1) & set(all_lists_2):
            matrix[x, y] = 1
            matrix[y, x] = 1
#将矩阵转化为DataFrame
matrix = pd.DataFrame(matrix)
#将fund_name作为矩阵的行索引
matrix.index = file_name_list
#将fund_name作为矩阵的列索引
matrix.columns = file_name_list
G = nx.Graph(matrix)
# 计算度中心度
degree_centrality = nx.degree_centrality(G)
# 计算紧密中心度
closeness_centrality = nx.closeness_centrality(G)
# 计算介数中心度
betweenness_centrality = nx.betweenness_centrality(G)
# 计算特征向量中心度
#eigenvector_centrality = nx.eigenvector_centrality(G)
#将上述四个中心度转化为DataFrame
# 设置图像大小为长 1000 像素宽 1000 像素
plt.figure (figsize=(10, 10))
# 定义节点颜色和透明度
nx.draw(G, with_labels=False,node_color='#144a74',node_size=100, edge_color='grey', width=0.1, alpha=0.5)
plt.show()
