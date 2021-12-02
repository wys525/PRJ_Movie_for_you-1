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

titles = []
reviews = []

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

for i in range(1, 50):
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2018&page={}'.format(i)
    try:
        driver.get(url)
        for j in range(1, 21):
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
            title = driver.find_element_by_xpath(movie_title_xpath).text
            print(title)
            titles.append(title)
            driver.find_element_by_xpath(movie_title_xpath).click()
            driver.find_element_by_xpath(review_button_xpath).click()
            review_range = driver.find_element_by_xpath(review_number_xpath).text.replace(',', '')
            review_range = review_range
            review_range = int(review_range)
            review_range = review_range // 10 + 2
            for k in range(1, review_range):
                review_page_url = driver.find_element_by_xpath(review_button_xpath).get_attribute('href')
                driver.get(review_page_url + '&page={}'.format(k))
                for l in range(1, 11):
                    review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)
                    try:
                        driver.find_element_by_xpath(review_title_xpath).click()
                        review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
                        print('===================== =====================')
                        print(review)
                        driver.back()
                    except:
                        driver.get(url)
                        break

    except:
        print('error')







