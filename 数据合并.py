import numpy as np
import pandas as pd
#导入文件夹中所有的csv文件
import os
file_path = "E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\Result"
file_list = os.listdir(file_path)
file_list_csv = [file for file in file_list if file.endswith('.csv')]
#建立空数据框
data = pd.DataFrame()
for file in file_list_csv:
    temp_data = pd.read_csv(file_path + "\\" + file)
    #将date列提取为年月日三列
    temp_data['date'] = pd.to_datetime(temp_data['date'])
    temp_data['year'] = temp_data['date'].dt.year
    temp_data['month'] = temp_data['date'].dt.month
    temp_data['day'] = temp_data['date'].dt.day
    #将month列中值为6的行删除
    temp_data = temp_data[temp_data['month'] != 6]
    #只保留code,year,macro_index列
    temp_data = temp_data[['code','year','macro_index']]
    #追加到data数据框
    data = pd.concat([data,temp_data],axis=0)

data.to_csv("E:\\论文工作区\\MacroCognition\\CMDA_管理层讨论与分析_ALL\\Result\\data.csv",index=False)