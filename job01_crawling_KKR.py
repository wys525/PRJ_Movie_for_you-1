from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options=webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('lang=ko_KR')
options.add_argument('disable_gpu')

driver=webdriver.Chrome('./chromedriver', options=options)


#https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=1
#https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=2~37
##영화 제목: //*[@id="old_content"]/ul/li[1]/a
#//*[@id="old_content"]/ul/li[2]/a
#//*[@id="old_content"]/ul/li[20]/a
#//*[@id="movieEndTabMenu"]/li[6]/a/em 리뷰버튼
#//*[@id="movieEndTabMenu"]/li[6]/a 리뷰 버튼 전체
#//*[@id="reviewTab"]/div/div/div[2]/span/em 리뷰건수
#//*[@id="pagerTagAnchor2"]/span 리뷰 페이지 숫자 버튼
##//*[@id="pagerTagAnchor2"] 리뷰 페이지 전체 버튼
#//*[@id="reviewTab"]/div/div/ul/li/a/strong 리뷰제목

review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
try:
    for i in range(1,38):
        url='https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page={}'.format(i)
        titles = []
        reviews = []

        for j in range(1,21): #영화갯수
            print(j+((i-1)*20),'번째 영화 크롤링 중')
            try:
                driver.get(url)
                movie_title_xpath='//*[@id="old_content"]/ul/li[{}]/a'.format(j)
                title=driver.find_element_by_xpath(movie_title_xpath).text
                driver.find_element_by_xpath(movie_title_xpath).click()
                # driver.find_element_by_xpath(review_button_xpath).click()
                review_page_url = driver.find_element_by_xpath(review_button_xpath).get_attribute('href')
                driver.get(review_page_url)
                # review_range=driver.find_element_by_xpath(review_number_xpath).text
                review_range=driver.find_element_by_xpath(review_number_xpath).text.replace(',','')
                review_range=review_range
                review_range=int(review_range)
                review_range=review_range//10+2
                if review_range>6:review_range=6 ##리뷰 페이지가 11페이지 이상이면 11페이까지만 긁어온다

                for k in range(1,review_range):
                    driver.get(review_page_url + '&page={}'.format(k))
                    time.sleep(0.5)
                    for l in range(1,11):
                        review_title_xpath='//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)
                        try:
                            driver.find_element_by_xpath(review_title_xpath).click()
                            time.sleep(0.5)
                            review=driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
                            # print('==============================================================================')
                            # print(title)
                            # print(review)
                            titles.append(title)
                            reviews.append(review)
                            driver.back()
                        except:
                            # print(l, '번째 review가 없다')
                            break


            except:
                print('error')
        df_review_20=pd.DataFrame({'title':titles, 'reviews':reviews})
        df_review_20.to_csv('./Crawling_N_movies/reviews_{}_{}.csv'.format(2020,i),
                            index=False)

##한방에 저장하는 코드(위험)
# df_review=pd.DataFrame({'title':titles, 'reviews':reviews})
# df_review.to_csv('./Crawling_N_movies/reviews_{}.csv'.format(2020))
except:
    print('total error')
finally:
    driver.close()

