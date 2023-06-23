'''
Description: 量化交易
Author: xiaoxinpro13
Date: 2021-08-20 09:59:00
LastEditTime: 2021-08-20 10:00:00
'''
from pandas_datareader import data as dt
import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#指定下载股票的日期范围
start_date ='20200501'
end_date='20210820'
#使用datareader从yahoo数据源获取数据
#将时间范围作为参数传入
pro = ts.pro_api('638281c86279705a0796bf6d4112c4db06161f8c90efa8ddee29cfa2')
zgpa = pro.daily(ts_code='000818.SZ', start_date=start_date, end_date=end_date)
#检查是否下载成功
zgpa.head()
#下面我们来创建交易信号
#为了不影响原始数据，这里创建一个新的数据表
#只保留原始数据中的日期index
zgpa.set_index('trade_date',inplace=True)
zgpa_signal=pd.DataFrame(zgpa.trade_date)
#为了更能体现股票的真实价值
#使用pre_close价格作为股票价格
zgpa_signal['price']=zgpa['pre_close']
#增加一个字段，存储股价的变化
zgpa_signal['diff']=zgpa_signal['price'].diff()
#增加diff字段后，第一行会出现空值，我们使用0来进行填补
zgpa_signal=zgpa_signal.fillna(0.0)
#如果股价上涨或不变，则标记为0
#如果股价下跌，则标记为1
zgpa_signal['signal']=np.where(zgpa_signal['diff']>0,0,1)
#接下来，根据交易信号的变化进行下单
#一般情况下，在A股市场，买入或卖出至少为100股，即1手
zgpa_signal['order']=zgpa_signal['signal'].diff()*100
#检查下单情况
zgpa_signal.head()



#考虑到股价较高，我们初始给小瓦2万元人民币让她去交易
initial_cash=20000.00
#增加一个字段，代表小瓦交易的股票的市值
zgpa_signal['stock']=zgpa_signal['order']*zgpa_signal['price']
#两次买卖的订单变化之差就是某一时刻小瓦仓位的变化情况
#持仓股票的数量变化乘以现价，就是小瓦交易产生的现金流
#用初始资金减去现金流变化的累加，就是小瓦剩余的现金
zgpa_signal['cash']=initial_cash-(zgpa_signal['order'].diff()*zgpa_signal['price']).cumsum()
#而股票的市值加上剩余的现金，就是小瓦的总资产
zgpa_signal['total']=zgpa_signal['stock']+zgpa_signal['cash']
#为了让小瓦直观看到自己的总资产变化
#我们用图形来进行展示
#设置图形的尺寸是10*6
plt.figure (figsize=(10,6))
#分别绘制总资产和持仓股票市值的变化
plt.plot(zgpa_signal['total'])
plt.plot(zgpa_signal['order'].cumsum()*zgpa_signal['price'],'--',label='stock value')
#增加网格，调整一下图注的位置，就可以显示图像了
plt.grid()
plt.legend(loc='center right')
plt.show()

#这里使用10日均线
period = 10
#设置一个空列表，用来存储每10天的价格
avg_10 = []
#再设置一个空列表，用来存储每10天价格的均值
avg_value = []
#设置一个循环
for price in zgpa['pre_close']:
    #把每天的价格传入avg_10列表
    avg_10.append(price)
    #当列表中存储的数值多于10个时
    if len(avg_10) > period:
    #就把前面传入的价格数据删除，确保列表中最多只有10天的数据
        del avg_10[0]
    #将10天数据的均值传入avg_value列表中
    avg_value.append(np.mean(avg_10))
#把计算好的10日均价写到股票价格数据表中
zgpa = zgpa.assign(avg_10 = pd.Series(avg_value, index = zgpa.index))
#检查一下是否添加成功
zgpa.head()
#设置图像尺寸为10*6
plt.figure(figsize=(10,6))
#绘制股价的变化
plt.plot(zgpa['pre_close'],lw=2,c='k')
#绘制10日均线
plt.plot(zgpa['avg_10'],'--',lw=2,c='b')
#添加图注和网格
plt.legend()
plt.grid()
#将图像进行显示
plt.show()

#新建一个数据表，命名为strategy(策略)
#序号保持和原始数据一致

#如何将zgpa的index设置为trade_date？
#答：
zgpa.set_index('trade_date',inplace=True)
strategy = pd.DataFrame(index=zgpa.index)
#添加一个signal字段，用来存储交易信号
strategy['signal']=0
#将5日均价保存到avg5这个字段
strategy['avg_5']=zgpa['pre_close'].rolling(5).mean()
#同样，将10日均价保存到avg10
strategy['avg_10']=zgpa['pre_close'].rolling(10).mean()
#当5日均价大于10日均价时，标记为1
#反之标记为0
strategy['signal']=np.where(strategy['avg_5']>strategy['avg_10'],1,0)
#根据交易信号的变化下单，当交易信号从0变成1时买入
#当交易信号从1变成0时卖出
#交易信号不变时不下单
strategy['order']=strategy['signal'].diff()
#查看数据表后10行
strategy.tail(10)
#创建尺寸为10*5的画布
plt.figure(figsize=(10,5))
#使用实线绘制股价
plt.plot(zgpa['pre_close'],lw=2,label='price')
#使用虚线绘制5日均线
plt.plot(strategy['avg_5'],lw=2,ls='--',label='avg5')
#使用一.风格绘制10日均线
plt.plot(strategy['avg_10'],lw=2,ls='-.',label='avglo')
#将买入信号用正三角进行标示
plt.scatter(strategy.loc[strategy.order==1].index,
zgpa['pre_close'][strategy.order==1],
marker = '^', s=80,color='r',label='Buy')
#将卖出信号用倒三角进行标示
plt.scatter(strategy.loc[strategy.order==-1].index,
zgpa['pre_close'][strategy.order==-1],
marker = 'v', s=80,color='g',label='Sell')
#添加图注
plt.legend()
#添加网格以便于观察
plt.grid()
#显示图像
plt.show()

#这次我们还是给小瓦2万元钱的启动资金
initial_cash = 20000
#新建一个数据表positions，序号和strategy数据表保持一致
#用0替换空值
positions = pd.DataFrame(index = strategy.index).fillna(0)
#因为A股买卖都是最低100股
#因此设置stock字段为交易信号的100倍
positions['stock'] = strategy['signal'] * 100
#创建投资组合数据表，用持仓的股票数量乘以股价得出持仓的股票市值
portfolio = pd.DataFrame(index = strategy.index)
portfolio['stock value'] = positions.multiply(zgpa['pre_close'], axis=0)
#同样仓位的变化就是下单的数量
order = positions.diff()
#用初始资金减去下单金额的总和就是剩余的资金
portfolio['cash'] = initial_cash -  order.multiply(zgpa['pre_close'],axis=0).cumsum()
#剩余的资金+持仓股票市值即总资产
portfolio['total'] = portfolio['cash'] + portfolio['stock value']
#检查一下后10行
portfolio.tail(10)
#创建10*5的画布
plt.figure (figsize=(10,5))
#绘制总资产曲线
plt.plot (portfolio['total'],lw=2,label='total')
#绘制持仓股票市值曲线
plt.plot (portfolio['stock value'],lw=2,ls='--',label='stock value')
#添加图注
plt.legend()
#添加网格
plt.grid()
#展示图像
plt.show()