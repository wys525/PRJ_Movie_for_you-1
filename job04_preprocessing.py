import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/naver_movie_reviews_onesentence_2015_2021.csv')
okt = Okt()
stopwords = pd.read_csv('./crawling_data/stopwords.csv', index_col=0)

cleaned_sentences = []
for sentence in df.reviews:
    sentence = re.sub('[^가-힣 ]', '', sentence)
    token = okt.pos(sentence, stem=True)
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_cleaned_token = df_token[(df_token['class'] == 'Noun') | df_token[(df_token['class'] == '') | df_token[(df_token['class'] == 'Noun')


