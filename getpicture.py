
import re

# 打开 HTML 文件，读取其中的内容
with open("F:\\Calibre\\Unknown\\Lai !Zhe Yang Xue She Ying _Cong Xia (86)\\Lai !Zhe Yang Xue She Ying _Cong Xia\\Lai !Zhe Yang Xue She Ying _Cong Xiang Fa Dao Jia Zuo Dan Sheng.html", 'r',encoding='utf8') as file:
    html_content = file.read()

# 查找所有以小写字母开头的单词，并将它们组成列表
matches = re.findall(r'https://res.weread.qq.com/.*?"', html_content)
for i in range(len(matches)):
    matches[i] = matches[i][0:-1]

matches = list(set(matches))

# 下载图片
import urllib.request
for url in matches:
    file_name = url.split('/')[-1]
    print("正在下载：", file_name)
    urllib.request.urlretrieve(url, file_name)
print("下载完成！")
