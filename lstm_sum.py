import numpy as np
import pandas as pd
 
data_policy = pd.read_excel("F:\\WeChat_Files\\WeChat Files\\xiaowenhao090238\\FileStorage\\File\\2023-07\\政策12.xlsx")#读取数据
data_eco = pd.read_excel("F:\\WeChat_Files\\WeChat Files\\xiaowenhao090238\\FileStorage\\File\\2023-07\\宏观经济12.xlsx")#
data_policy.to_csv("F:\\WeChat_Files\\WeChat Files\\xiaowenhao090238\\FileStorage\\File\\2023-07\\政策12.csv",index=False)
data_eco.to_csv("F:\\WeChat_Files\\WeChat Files\\xiaowenhao090238\\FileStorage\\File\\2023-07\\宏观经济12.csv",index=False)
data_policy = pd.read_csv("F:\\WeChat_Files\\WeChat Files\\xiaowenhao090238\\FileStorage\\File\\2023-07\\政策12.csv")
data_eco = pd.read_csv("F:\\WeChat_Files\\WeChat Files\\xiaowenhao090238\\FileStorage\\File\\2023-07\\宏观经济12.csv")
#将数据框按照日期列分类对bilstm预测列进行求和
positive_sum = data_policy[data_policy['bilstm预测'] > 0].groupby('日期')['bilstm预测'].sum()
negative_sum = data_policy[data_policy['bilstm预测'] < 0].groupby('日期')['bilstm预测'].sum()
#将两个数据框按日期列匹配合并
data_policy1 = pd.merge(positive_sum,negative_sum,on='日期')
positive_sum2 = data_eco[data_eco['bilstm预测'] > 0].groupby('日期')['bilstm预测'].sum()
negative_sum2 = data_eco[data_eco['bilstm预测'] < 0].groupby('日期')['bilstm预测'].sum()
data_eco1 = pd.merge(positive_sum2,negative_sum2,on='日期')
data_policy1.to_excel("F:\\WeChat_Files\\WeChat Files\\xiaowenhao090238\\FileStorage\\File\\2023-07\\政策12统计.xlsx")
data_eco1.to_excel("F:\\WeChat_Files\\WeChat Files\\xiaowenhao090238\\FileStorage\\File\\2023-07\\宏观经济12统计.xlsx")
#将两个数据框按日期列匹配合并