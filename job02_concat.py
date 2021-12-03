import pandas as pd

# df = pd.read_csv('./crawling_data/reviews_2016_1.csv')
#
# for i in range(2, 60):
#     df_temp = pd.read_csv('./crawling_data/reviews_2016_{}.csv'.format(i))
#     df_temp.dropna(inplace=True)
#     df_temp.drop_duplicates()
#     # df_temp.columns = ['title','reviews']
#     # df_temp.to_csv('./crawling_data/reviews_2016_{}.csv'.format(i),index=False)
#     df = pd.concat([df, df_temp], ignore_index=True)
# df.info()
# df.to_csv('./crawling_data/reviews_2016.csv')

df = pd.DataFrame()

for i in range(15, 22):
    df_temp = pd.read_csv('./crawling_data/reviews_20{}.csv'.format(i))
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df_temp.columns = ['title', 'reviews']
    df_temp.to_csv('./crawling_data/reviews_20{}.csv'.format(i), index=False)
    df = pd.concat([df, df_temp], ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()
df.to_csv('./crawling_data/naver_movie_reviews_2015_2021.csv')