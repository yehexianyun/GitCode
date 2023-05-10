import pandas as pd
import numpy as np
import os
# 指定文件夹路径
folder_path = r'G:\\12_Database\\CMDA_管理层讨论与分析_ALL\\2021\\文本\\文本'
# 获取文件夹中所有文件名
data = pd.DataFrame()
data['code'] = []
file_names = os.listdir(folder_path)
data['path'] = file_names
data['code'] = data['path'].apply(lambda x: x[:6])
data['date'] = data['path'].apply(lambda x: x[7:17])

#分句
for file_name in os.listdir(folder_path):
    if file_name.endswith('.txt'):
        with open(os.path.join(folder_path, file_name), 'r') as f:
            # 在这里进行文件操作
            text =
            pass

