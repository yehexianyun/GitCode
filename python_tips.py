#python 变量解包
usernames = ['piglei', 'raymond']
author, reader = usernames
#赋值语句左侧添加小括号 (...)，甚至可以一次展开多层嵌套数据。
attrs = [1, ['piglei', 100]]
user_id, (username, score) = attrs
#动态解包
data = ['piglei', 'apple', 'orange', 'banana', 100]
username, *fruits, score = data
