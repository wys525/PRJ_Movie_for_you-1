''' 2018년 개봉 영화 리뷰 크롤링 '''

from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)

# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=1
# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=2   37까지
# 영화 제목 xpath
# //*[@id="old_content"]/ul/li[1]/a
# //*[@id="old_content"]/ul/li[2]/a
# //*[@id="old_content"]/ul/li[20]/a
# //*[@id="movieEndTabMenu"]/li[6]/a/em  리뷰버튼,
# //*[@id="reviewTab"]/div/div/div[2]/span/em 리뷰 건수

# //*[@id="pagerTagAnchor1"]   리뷰 페이지 버튼
# //*[@id="pagerTagAnchor10"]/em   리뷰 다음 페이지 버튼
# //*[@id="reviewTab"]/div/div/ul/li[1]/a/strong 리뷰 제목
# //*[@id="SE-ec9bce5c-9be3-47a9-9957-b075426d88fb"] 리뷰 한 줄
# //*[@id="content"]/div[1]/div[4]/div[1]/div[4]        # class:user_tx_area


review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
try:
    for i in range(1, 51): #2018년 총 998개 * 페이지당 20개 영화 * 총 50페이지
        url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2018&page={}'.format(i)
        titles = []
        reviews = []
        for j in range(1, 21):
            print(j+((i-1)*20), '번째 영화 크롤링 중 >>>>>>>>>>>>>>>')
            try:
                driver.get(url)
                movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
                title = driver.find_element_by_xpath(movie_title_xpath).text
                driver.find_element_by_xpath(movie_title_xpath).click()
                driver.find_element_by_xpath(review_button_xpath).click()
                review_range = driver.find_element_by_xpath(review_number_xpath).text.replace(',', '') # 1000개가 넘어가면 콤마가 찍혀서 int값으로 안되기 떄문에 그걸 빼는거임.
                review_range = review_range
                review_range = int(review_range)
                review_range = review_range // 10 + 2
                if review_range > 6: review_range = 6  #리뷰 50개까지만 최대 긁어오게... 5페이에 있는 리뷰까지! 제한함.
                for k in range(1, review_range):
                    review_page_url = driver.find_element_by_xpath(review_button_xpath).get_attribute('href') #get_attribute()에 클래스등 속성명을 가져옴. 속석명을 써주면됨.
                    driver.get(review_page_url + '&page={}'.format(k))
                    for l in range(1, 11):
                        review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)
                        try:
                            driver.find_element_by_xpath(review_title_xpath).click()
                            time.sleep(0.3)
                            review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
                            print('===================== =====================')
                            # print(title)  # 제목 찍어주고
                            # print(review) # 리뷰 찍어주고
                            titles.append(title) # 타이틀 매 리뷰마다 찍게하기 위해서 이 안에 넣음.
                            reviews.append(review) # 리뷰내용 더하기 . append 하는 애들은 몰아놔야 title과 review가 짝이 맞게됨. 에러나도 붙어있게...에러날거 없을때에만 append 해줄 것.
                            driver.back()
                        except:
                            print(1, '번째 review가 없습니다')
                            break

            except:
                print('error')
        # 중간 저장 코드 넣기. 영화 20개 크롤링 할 때마다 저장할거임.
        df_review_20 = pd.DataFrame({'title':titles, 'reviews':reviews})
        df_review_20.to_csv('./crawling_data/reviews_{}_{}.csv'.format(2018, i))
except:
    print('totally error')
finally:                                # 에러가 나든 작동을 하든 다 하고나면 아래 명령을 작동함.
    driver.close()
# 저장하기. 다 끝나고 한번에 저장
# df_review = pd.DataFrame({'title':titles, 'reviews':reviews})
# df_review.to_csv('./crawling_data/reviews_{}.csv'.format(2018))

#저장할 떄 index = False 안줬음.