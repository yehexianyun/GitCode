# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:44:59 2022

@author: yehe
"""
#%%
def pdf_download(code,year):
    import tushare as ts
    ts.set_token('638281c86279705a0796bf6d4112c4db06161f8c90efa8ddee29cfa2')
    pro = ts.pro_api()
    pdf_df = pro.anns(**{
        "ts_code": '000002.SZ',
        "ann_date": "",
        "start_date": "20130101",
        "end_date": "20130630",
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "ann_date",
        "filepath",
        "src_url",
        "ann_type",
        "title"
    ])
    pdf_df.loc[:, 'match1'] = ""
    pdf_df.loc[:, 'match2'] = ""
    pdf_df.loc[:, 'match3'] = ""
    import re
    for i in range(len(pdf_df["title"])):
        if re.match('\w*（已取消）',pdf_df["title"][i]) == None:
            pdf_df["match1"][i] =  0
    for j in range(len(pdf_df["title"])):
        if re.match('\w*摘要',pdf_df["title"][j]) == None:
            pdf_df["match2"][j] =  0
    for j in range(len(pdf_df["title"])):
        if re.match('\w*关于',pdf_df["title"][j]) == None:
            pdf_df["match3"][j] =  0
    pdf_df_new = pdf_df.loc[(pdf_df['ann_type'] == '年度报告')&(pdf_df['match1'] == 0)&(pdf_df['match2'] == 0)&(pdf_df['match3'] == 0)]
    pdf_df_new.index = range(len(pdf_df_new)) #重设索引
    url = pdf_df_new['src_url']
    name = pdf_df_new['filepath'] 
    #下载文件
    for i in range(len(url)):
        r = requests.get(url[i], stream=True)
        with open('D:\\Files\\nianbao\\'+name[i], 'wb') as f:
            f.write(r.content)
    #return name[i]
    
pdf_download('000002.SZ','2012')
#%%            
import re
import requests
import tushare as ts
ts.set_token('638281c86279705a0796bf6d4112c4db06161f8c90efa8ddee29cfa2')
pro = ts.pro_api()
#获取股票代码
code_df = pro.stock_basic(**{
    "ts_code": "",
    "name": "",
    "exchange": "",
    "market": "",
    "is_hs": "",
    "list_status": "",
    "limit": "",
    "offset": ""
}, fields=[
    "ts_code",
    "symbol",
    "name",
    "area",
    "industry",
    "market",
    "list_date",
    "list_status"
])
code_df.index = range(len(code_df))
ts_code = code_df['ts_code']
#下载文件
for i in range(10):
    for j in range(2012,2021):
        pdf_download(ts_code[i],str(j))
        print(ts_code[i]+str(j)+"下载完成")
#%%
#判断提取方式
import os
import re
import fitz
import shutil
file_dir = r'D:\\Files'
for files in os.walk(file_dir):
    files_list = files[2]
pdfs_1 = [] 
pdfs_2 = []
pdfs_3 = []
others = []   
text_all = []
for i in range(5):
    pdf = fitz.open(file_dir+'\\'+ files_list[2])
    for page in pdf:
        text = page.get_text("text")
        text_all.append(text)
    text_all = ''.join(text_all)
    if '董事\w报告' in text_all:
        pdfs_1.append(files_list[2])
    elif '管理层讨论与分析' in text_all:
        pdfs_2.append(files_list[2])
    elif '公司经营情况讨论' in text_all:
        pdfs_3.append(files_list[2])
    else:
        others.append(files_list[2])
# 移入相应文件夹
for item in pdfs_1:
    newpath = 'D:\\Files\\1\\' + item.split('\\')[-1]
    os.rename(file_dir+'\\'+ files_list[2], newpath)  
for item in pdfs_2:
    newpath = 'D:\\Files\\2\\' + item.split('\\')[-1]
    os.rename(item,newpath)            
for item in pdfs_3:
    newpath = 'D:\\Files\\3\\' + item.split('\\')[-1]
    os.rename(item,newpath)
for item in others:
    newpath = 'D:\\Files\\4\\' + item.split('\\')[-1]
    os.rename(item,newpath)    
#%%
# pdf转HTML
import fitz
import tqdm
import sys
def pdf2html(input_path,html_path):
    doc = fitz.open(input_path)
    for page in tqdm.tqdm(doc):
        html_content = page.get_text("html")
        with open(html_path, 'a', encoding='utf8', newline="") as fp:
            fp.write(html_content) 

file_dir_1 = r'D:\\Files\\1'
for files in os.walk(file_dir_1):
    files_list_1 = files[2]

input_path = []
output_path = []
for i in range(len(files_list_1)):
    input_path.append(file_dir_1+r'\\'+ files_list_1[i])
for i in range(len(files_list_1)):
    output_path.append(file_dir+r'\\网页\\'+ files_list_1[i]+'.html')

input_path_new = list(set(input_path))
output_path_new = list(set(output_path))
for i in range(len(input_path)):
               pdf2html(input_path_new[i],output_path_new[i])
#%%
# 判断标题字号
from bs4 import BeautifulSoup
def font_size(path):
    soup=BeautifulSoup(open(output_path_new[1],encoding='utf-8'),features='html.parser')
    new_txt = soup.prettify()
    import re
    p_title = r'font-size:(.*?)pt\">\s*\w*\s*董事会报告'
    result = re.findall(p_title,new_txt)
    font_list = []
    for i in result:
        font_list.append(float(i))
        font_size_result = max(font_list)
        if font_size_result.is_integer():
            font_size_txt = str(int(font_size_result))
            re_font_size_txt = font_size_txt
        else:
            font_size_txt = str(font_size_result)
            re_font_size_txt = font_size_txt.replace(r'.',r'\.')
    
    return re_font_size_txt
print(font_size(output_path_new[1]))
#%%
# 提取内容
import re
import pandas as pd
df_content = pd.DataFrame(columns=['ts_code','year','neg','pos','all','sentence'])
def content(path):
    p_content_1 = r"font-size:"+font_size(path)+r"pt\">\s*\w*\s*董事会报告(.*?)"+font_size(path)+r"pt\">\s*第"
    soup=BeautifulSoup(open(path,encoding='utf-8'),features='html.parser')
    new_txt = soup.prettify()
    new_txt = soup.prettify()
    content = re.findall(p_content_1,new_txt,re.S)
    new_content =''.join(content)
    new_content = re.sub('<.*?>','',new_content)
    new_content = re.sub('\n','',new_content)
    new_content = re.sub(' ','',new_content)
    new_content = re.sub('<span.*?size:','',new_content)
    return new_content
    
new_content = content(r'D:\\Files\\1\\000001.SZ_20140307_2013年年度报告.pdf.html')

df_new = pd.DataFrame({'ts_code':[output_path[0][14:24]],'year':[output_path[0][33:38]],\
                       'neg':[neg_word(new_content)],\
                           'pos':[pos_word(new_content)],\
                               'all':[words(new_content)],
                               'sentence':[sentence(new_content)]})
df_content.loc[0] = [output_path[0][14:24],output_path[0][33:38],neg_word(new_content),pos_word(new_content),words(new_content),sentence(new_content)]
#%%
# 语义分析
import os 
import jieba
import sys
from unicodedata import category
import pandas as pd
jieba.load_userdict(r'C:\Users\yehe\Desktop\jieba.txt')
# 切分句子并统计句子总数
cut_1 = r'，|。|？' #设定句子切分标点
sentence = re.split(cut_1,new_content)
all_sentence = len(sentence)
wordlist=jieba.lcut(new_content) #cut_all=Flase
word_list = list(wordlist)
codepoints = range(sys.maxunicode + 1)
punctuation = {c for i in codepoints if category(c := chr(i)).startswith("P")}
word_list_1 = [_ for _ in wordlist if _ not in punctuation and _ != ' ' and len(_) >= 2]
word_amount = len(word_list_1)
with open('C:\\Users\\yehe\\Desktop\\neg.txt', encoding='utf-8') as file:
     neg_word=file.read()
neg_word_list = neg_word.split('\n')
neg_word_amount = 0
for it in neg_word_list:
    for t in word_list_1:
        if it == t:
            neg_word_amount += 1
with open('C:\\Users\\yehe\\Desktop\\pos.txt', encoding='utf-8') as file:
     pos_word=file.read()            
pos_word_list = pos_word.split('\n')
pos_word_amount = 0
for it in pos_word_list:
    for t in word_list_1:
        if it == t:
            pos_word_amount += 1            

def sentence(content):
    import os 
    import jieba
    import sys
    from unicodedata import category
    import pandas as pd
    jieba.load_userdict(r'C:\Users\yehe\Desktop\jieba.txt')
    # 切分句子并统计句子总数
    cut_1 = r'，|。|？' #设定句子切分标点
    sentence = re.split(cut_1,new_content)
    all_sentence = len(sentence)
    return all_sentence

def words(content):
    import os 
    import jieba
    import sys
    from unicodedata import category
    import pandas as pd
    jieba.load_userdict(r'C:\Users\yehe\Desktop\jieba.txt')
    wordlist=jieba.lcut(new_content) #cut_all=Flase
    word_list = list(wordlist)
    codepoints = range(sys.maxunicode + 1)
    punctuation = {c for i in codepoints if category(c := chr(i)).startswith("P")}
    word_list_1 = [_ for _ in wordlist if _ not in punctuation and _ != ' ' and len(_) >= 2]
    word_amount = len(word_list_1)
    return word_amount

def neg_word(content):
    import os 
    import jieba
    import sys
    from unicodedata import category
    import pandas as pd
    jieba.load_userdict(r'C:\Users\yehe\Desktop\jieba.txt')
    wordlist=jieba.lcut(new_content) #cut_all=Flase
    word_list = list(wordlist)
    codepoints = range(sys.maxunicode + 1)
    punctuation = {c for i in codepoints if category(c := chr(i)).startswith("P")}
    word_list_1 = [_ for _ in wordlist if _ not in punctuation and _ != ' ' and len(_) >= 2]
    with open('C:\\Users\\yehe\\Desktop\\neg.txt', encoding='utf-8') as file:
         neg_word=file.read()
    neg_word_list = neg_word.split('\n')
    neg_word_amount = 0
    for it in neg_word_list:
        for t in word_list_1:
            if it == t:
                neg_word_amount += 1
    return neg_word_amount

def pos_word(content):
    import os 
    import jieba
    import sys
    from unicodedata import category
    import pandas as pd
    jieba.load_userdict(r'C:\Users\yehe\Desktop\jieba.txt')
    wordlist=jieba.lcut(new_content) #cut_all=Flase
    word_list = list(wordlist)
    codepoints = range(sys.maxunicode + 1)
    punctuation = {c for i in codepoints if category(c := chr(i)).startswith("P")}
    word_list_1 = [_ for _ in wordlist if _ not in punctuation and _ != ' ' and len(_) >= 2]
    with open('C:\\Users\\yehe\\Desktop\\pos.txt', encoding='utf-8') as file:
         pos_word=file.read()            
    pos_word_list = pos_word.split('\n')
    pos_word_amount = 0
    for it in pos_word_list:
        for t in word_list_1:
            if it == t:
                pos_word_amount += 1 
    return pos_word_amount
#%% 
import re
import requests
import tushare as ts
ts.set_token('638281c86279705a0796bf6d4112c4db06161f8c90efa8ddee29cfa2')
pro = ts.pro_api()
#获取股票代码
code_df = pro.stock_basic(**{
    "ts_code": "",
    "name": "",
    "exchange": "",
    "market": "",
    "is_hs": "",
    "list_status": "",
    "limit": "",
    "offset": ""
}, fields=[
    "ts_code",
    "symbol",
    "name",
    "area",
    "industry",
    "market",
    "list_date",
    "list_status"
])
ts_code = code_df['ts_code']
code_df['path'] = ''
#下载文件
for i in range(10):
    for j in range(2012,2021):
        pdf_download(ts_code[i],str(j))
        print(ts_code[i]+str(j)+"下载完成")
#%%汇总
content_path = output_path_new
#清除无效路径
for item in content_path:
    if re.match('html{1}',item) == None:
        content_path.remove(item)

df_content = pd.DataFrame(columns=['ts_code','year','neg','pos','all','sentence'])
for i in range(len(content_path)):
    new_content = content(content_path[i])
    df_content.loc[i] = [content_path[i][15:24],content_path[i][34:38],neg_word(new_content),pos_word(new_content),words(new_content),sentence(new_content)]
    
                  