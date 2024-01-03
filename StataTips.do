**# stata框架集
// 设置参数
global github "https://raw.githubusercontent.com/zhangdashenqi"
webuse set "${github}/the_zen_of_stata/master/data"

// 载入股票数据
webuse stock.dta, clear
frame create 账面价值 //创建一个名为账面价值的数据框；
frame 账面价值: webuse bookValue.dta, clear //指定在账面价值数据框中执行webuse bookValue.dta, clear命令，用于载入bookValues.dta数据集。
frame dir   // 查询内存中的所有数据框
frame rename default 股票数据 //将default命名为股票数据
frame pwf      // 查询当前工作的数据框