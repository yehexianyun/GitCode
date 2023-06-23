import os
import pandas as pd

folder_path2 = "G:\\12_Database\\新闻数据"

# 获取文件夹中的所有excel文件
file_list = [f for f in os.listdir(folder_path2) if f.endswith('.xlsx')]

# 创建一个空的dataframe
df2 = pd.DataFrame()

# 循环读取每个excel文件并将其添加到dataframe中
for file in file_list:
    file_path = os.path.join(folder_path2, file)
    temp_df2 = pd.read_excel(file_path)
    temp_df2.columns = ['date', 'title', 'source']
    df2= pd.concat([df2, temp_df2], ignore_index=True)

9
# 设置文件夹路径
folder_path = "G:\\12_Database\\股吧文本数据"

# 获取文件夹中的所有pkl文件
file_list = [f for f in os.listdir(folder_path) if f.endswith('.pkl')]

# 创建一个空的dataframe
df = pd.DataFrame()

# 循环读取每个pkl文件并将其添加到dataframe中
for file in file_list:
    file_path = os.path.join(folder_path, file)
    temp_df = pd.read_pickle(file_path)
    df = pd.concat([df, temp_df], ignore_index=True)

df = df.iloc[:, [4, 6]]
df.columns = ['date', 'title']
data = pd.concat([df, df2], ignore_index=True)
df3 = pd.DataFrame(data['title'].astype(str))
data.to_csv("G:\\12_Database\\LDA_data.csv")
#LDA model
import gensim
from gensim import corpora
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import warnings
warnings.filterwarnings('ignore')  # To ignore all warnings that arise here to enhance clarity
 
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel

import jieba
def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))
df3["content_cutted"] = df3.title.apply(chinese_word_cut) #分词,并且去掉
df3.content_cutted.head()
# 
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
n_features = 1000
tf_vectorizer = CountVectorizer(strip_accents = 'unicode',
                                max_features=n_features,
                                stop_words='english',
                                max_df = 0.5,
                                min_df = 10)
tf = tf_vectorizer.fit_transform(df3.content_cutted)

from sklearn.decomposition import LatentDirichletAllocation
n_topics = 5 
lda = LatentDirichletAllocation(n_components=n_topics, max_iter=50,
                                learning_method='online',
                                learning_offset=50,
                                random_state=0)


lda.fit(tf)

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

n_top_words = 20

tf_feature_names = tf_vectorizer.get_feature_names_out()
print_top_words(lda, tf_feature_names, n_top_words)

import pyLDAvis
import pyLDAvis.sklearn

pyLDAvis.enable_notebook()
pic = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
pyLDAvis.display(pic)
pyLDAvis.save_html(pic, 'lda_pass'+str(n_topics)+'.html')

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

pyLDAvis.enable_notebook()
pic = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
pyLDAvis.display(pic)
pyLDAvis.save_html(pic, 'lda_pass'+str(n_topics)+'.html')

import pyLDAvis
import pyLDAvis.sklearn
pyLDAvis.enable_notebook()
pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
