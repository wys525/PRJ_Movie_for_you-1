from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()
# options.add_argument('headless') # 웹브라우저가 안뜬다.
options.add_argument('land=ko_KR')
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', options=options)



# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020
# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=1
# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=2 37까지

# //*[@id="old_content"]/ul/li[1]/a
# //*[@id="old_content"]/ul/li[2]/a
# //*[@id="old_content"]/ul/li[20]/a
# //*[@id="movieEndTabMenu"]/li[6]/a/em # 리뷰 버튼
# //*[@id="reviewTab"]/div/div/div[2]/span/em # 리뷰 개수
# //*[@id="reviewTab"]/div/div/ul/li[1]/a/strong 리뷰 제목
# //*[@id="pagerTagAnchor1"] 리뷰 페이지 버튼
# //*[@id="pagerTagAnchor2"]
# //*[@id="content"]/div[1]/div[4]/div[1]/div[4]/div # class="user_tx_area"

review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
try:
    for i in range(1, 38):
        url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page={}'.format(i)
        titles = []
        reviews = []

        for j in range(1, 21):
            print(j+((i-1)*20), '번째 영화 크롤링 중...')
            try:
                driver.get(url)
                movie_title_xpath ='//*[@id="old_content"]/ul/li[{}]/a'.format(j) # 영화 타이틀을 받아온다.
                title = driver.find_element_by_xpath(movie_title_xpath).text # 텍스트 파일 저장


                driver.find_element_by_xpath(movie_title_xpath).click()
                # driver.find_element_by_xpath(review_button_xpath).click() # 클릭은 믿을게 못된다.

                review_page_url = driver.find_element_by_xpath(review_button_xpath).get_attribute('href')  # href속성값을 가져온다. 주소다

                driver.get(review_page_url) #확실한건 driver get 속성값의 드라이버를 받아온다.
                review_range = driver.find_element_by_xpath(review_number_xpath).text.replace(',', '')
                 # 1000이 넘어가는 것중에 콤마를 뺌
                review_range = int(review_range)
                review_range = review_range // 10 + 2
                if review_range > 6:
                    review_range =6

                for k in range(1, review_range):

                    driver.get(review_page_url + '&page={}'.format(k)) # 페이지를 이어 붙여준다.
                    # time.sleep(0.3)
                    for l in range(1, 11):
                        review_title_xpath= '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)
                        try:
                            driver.find_element_by_xpath(review_title_xpath).click()
                            # time.sleep(0.3)
                            time.sleep(0.3)
                            review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
                            # print('========================= ==================')
                            # print(title)
                            # print(review)
                            titles.append(title)
                            reviews.append(review)
                            driver.back()
                        except:
                            print(l, '번째 review가 없다.')
                            # driver.get(url)
                            break
            except:
                print('error')

        df_review_20 = pd.DataFrame({'title': titles, 'reviews': reviews}) # 20 개씩저장
        df_review_20.to_csv('./crawling_data/reviews_{}_{}.csv'.format(2020, i), index=False)
except:
    print('totally error')
finally:
    driver.close()


# df_review = pd.DataFrame({'title':titles, 'reviews':reviews})
# df_review.to_csv('./crawling_data/reviews_{}.csv'.format(2020))
