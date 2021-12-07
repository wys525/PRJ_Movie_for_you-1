import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
from matplotlib import font_manager, rc
import matplotlib as mpl

font_path = './malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus']=False
rc('font', family=font_name)

embedding_model = Word2Vec.load('./models/word2VecModel_2015_2021.model')
key_word = '겨울'
sim_word = embedding_model.wv.most_similar(key_word, topn=100)
print(sim_word)

vectors = []
labels = []
for label, _ in sim_word:
    labels.append(label)
    vectors.append(embedding_model.wv[label])


df_vectors = pd.DataFrame(vectors)

tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23) # k.fold
new_value = tsne_model.fit_transform(df_vectors)
df_xy = pd.DataFrame({'words':labels, 'x':new_value[:, 0], 'y':new_value[:, 1]})
print(df_xy.head())
print(df_xy.shape)
df_xy.loc[df_xy.shape[0]] = (key_word, 0, 0)
print(df_xy.tail(11))

plt.figure(figsize=(8,8))
plt.scatter(0, 0, s=1500, marker='*')
for i in range(len(df_xy.x)):
    a = df_xy.loc[[i, 10], :]
    plt.plot(a.x, a.y, '-D', linewidth=2)
    plt.annotate(df_xy.words[i], xytext=(5, 2), xy=(df_xy.x[i], df_xy.y[i]), textcoords='offset points', ha='right', va='bottom') #annotate 그림 주석달기  한글이라 bottom
    plt.show()