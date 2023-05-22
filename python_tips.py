#python 变量解包
usernames = ['piglei', 'raymond']
author, reader = usernames
#赋值语句左侧添加小括号 (...)，甚至可以一次展开多层嵌套数据。
attrs = [1, ['piglei', 100]]
user_id, (username, score) = attrs
#动态解包
data = ['piglei', 'apple', 'orange', 'banana', 100]
username, *fruits, score
#解包时忽略变量
username, *_, score = data # _ 代表忽略变量，不会被赋值，也不会被使用
#函数说明文档
def func(data,items):
    """函数说明文档
    :param data: 数据
    :param items: 项目
    :return: 返回值
    :type data: str
    :type items: list"""
    pass
#变量命名的PEP8原则
https://peps.python.org/pep-0008/
#使用Decimal模块进行精确计算
from decimal import Decimal
Decimal('0.1') + Decimal('0.2') # Decimal('0.3')，一定使用字符串表示数字




