import pandas as pd
import numpy as np
import os
# 指定文件夹路径
folder_path = r'G:\\12_Database\\CMDA_管理层讨论与分析_ALL\\2021\\文本\\文本'
# 获取文件夹中所有文件名
data = pd.DataFrame()
data
file_names = os.listdir(folder_path)
for i in range(len(file_names)):
    data['code'][i] = file_names[i][:6]
    
# 打印文件名列表
print(file_names)

