import tomotopy as tp
import pickle
data =  pickle.load(open('df3.pkl', 'rb'))
def find_k(docs, min_k=1, max_k=10, min_df=2):
    # min_df 词语最少出现在2个文档中
    import matplotlib.pyplot as plt
    scores = []
    for k in range(min_k, max_k):
        print("current number of topics:", k)
        mdl = tp.LDAModel(min_df=min_df, k=k, seed=555)
        for words in docs:
            if words:
                mdl.add_doc(words)
        mdl.train(20)
        coh = tp.coherence.Coherence(mdl)
        scores.append(coh.get_score())
        
 
    plt.plot(range(min_k, max_k), scores)
    plt.xlabel("number of topics")
    plt.ylabel("coherence")
    plt.show()
      
find_k(docs=data['content_cutted'], min_k=1, max_k=10, min_df=2)