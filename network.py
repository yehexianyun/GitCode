import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
data = pd.read_excel("G:\\12_Database\\股票型基金-网络.xlsx")
#按照enddate分类拆分数据
#删除ReportTypeID列值为5或6的数据
data = data[(data['ReportTypeID'] != 5) & (data['ReportTypeID'] != 6)]
#取enddate列
enddate = data['EndDate']
#去重
enddate = enddate.drop_duplicates()
#对enddate每个值进行循环
for i in enddate:
    print(i)
    #选择enddate为i的数据
    data_new = data[data['EndDate'] == i]
    #重置索引
    data_new = data_new.reset_index(drop=True)
    #提取第一列的数值并去重
    fund = data_new['MasterFundCode'].drop_duplicates()
    dict_fund = {
        j: set(
            data_new[data_new['MasterFundCode'] == j][
                'Symbol'
            ].drop_duplicates()
        )
        for j in fund
    }
    all_lists = [list(value_) for value_ in dict_fund.values()]
    #新建一个空矩阵
    #矩阵行数与列数为j
    #矩阵元素为0
    matrix = np.eye((len(fund)))
    # 比较两两列表之间是否有相同元素
    for x in range (len(fund)):
        for y in range (x+1, len(fund)):
            if set (all_lists[x]) & set (all_lists [y]):
                matrix [x, y] = 1
                matrix [y, x] = 1
    #将矩阵转化为DataFrame
    matrix = pd.DataFrame(matrix)
    #将fund_name作为矩阵的行索引
    matrix.index = fund
    #将fund_name作为矩阵的列索引
    matrix.columns = fund
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
    degree_data = pd.DataFrame.from_dict(degree_centrality,orient='index',columns=['degree_centrality'])
    closeness_data = pd.DataFrame.from_dict(closeness_centrality,orient='index',columns=['closeness_centrality'])
    betweenness_data = pd.DataFrame.from_dict(betweenness_centrality,orient='index',columns=['betweenness_centrality'])
    #eigenvector_data = pd.DataFrame.from_dict(eigenvector_centrality,orient='index',columns=['eigenvector_centrality'])
    #将四个中心度合并为一个DataFrame,以fund_name为索引
    centrality_data = pd.concat([degree_data,closeness_data,betweenness_data],axis=1)
    #将centrality_data写入Excel文件，centrality_data为工作表名，并同时将matrix写入同一个Excel文件，matrix为工作表名
    writer = pd.ExcelWriter('G:\\12_Database\\股票型基金\\股票型基金网络矩阵'+str(i)+'.xlsx')
    centrality_data.to_excel(writer,'centrality_data')
    matrix.to_excel(writer,'matrix')
    #writer.save()
    with pd.ExcelWriter('G:\\12_Database\\股票型基金\\股票型基金网络矩阵'+str(i)+'.xlsx') as writer:
        centrality_data.to_excel(writer, sheet_name='centrality_data')
        matrix.to_excel(writer, sheet_name='matrix')
    print(i + '已完成')
#新建一个空数据框
data = pd.DataFrame()
