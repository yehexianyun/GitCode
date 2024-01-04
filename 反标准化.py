#导入csv文件取第二列数据
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv("F:\\WeChat_Files\\WeChat Files\\xiaowenhao090238\\FileStorage\\File\\2023-07\\h.csv",header=0)
# 取第三列数据
data2 = data.iloc[:,2]
#将data2转换为numpy数组
# 创建一个Series对象

# 创建StandardScaler对象
scaler = StandardScaler()

# 将Series转换为NumPy数组
array = data2.values.reshape(-1, 1)

# 对数组进行标准化
scaled_array = scaler.fit_transform(array)

# 使用inverse_transform()方法进行逆标准化
origen_data = scaler.inverse_transform(scaled_array)

# 将逆标准化后的数组转换为Series
inverse_scaled_series = pd.Series(inverse_scaled_array.flatten())

# 打印逆标准化后的Series
print(inverse_scaled_series)
