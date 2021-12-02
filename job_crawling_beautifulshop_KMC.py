import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv


url_pre = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=45290&type=after&onlyActualPointYn=N&onlySpoilerPointYn=N&order=sympathyScore&page='
id_list = []
id_pre = '_filtered_ment_'
final_data = []

for page in range(10):
    site = url_pre + str(page + 1)  # 1 ~ 10까지 변환됨.
    res = requests.get(site)

    soup = BeautifulSoup(res.content, 'html.parser')

    score_list = []
    scores = soup.find_all('div', 'star_score')
    for score in scores:
        score_list.append(score.get_text())

    for i in range(10):
        id_list.append(id_pre + str(i))

    mydata = []
    for id in id_list:
        mydata.append(soup.find('span', {'id': id}).get_text())

    for score, line in zip(score_list, mydata):
        final_data.append([score.strip(), line.strip()])

pd.DataFrame(final_data)
print()

'''위의 두 데이터를 하나의 데이터프레임으로 만들기 위해선 두 리스트 데이터를 하나의 리스트 데이터로 추가한 다음 
pandas의 데이터프레임으로 변환하는 것으로 코드를 작성하면 된다.

 id를 통해서 해당 요소에 접근하는 경우  soup.find('span',{'id' : id}) 로 작성한다.

 '''