from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions
# options.add.argument('headless') #크롤링동안 웹드라이버 안보이게 함.
options.add_argument("lang=ko_KR")
options.add_argument('disable_gpu')

driver = webdriver.Chrome('./chromedriver', option = options) #.exe는 빼고 적음.

titles = []
reviews = []

# main page url : https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020
# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2021
# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2019

# 1페이지 url : https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=1
# 2페이지 :     https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=2

# 한페이지당 20개씩, 37페이지는 20개가 안됨.


for i in range(1,38):
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page={}'.format(i)
    driver.get(url)
    for j in range(1,21):
        try:
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
            title = driver.find_element_by_xpath(movie_title_xpath).text
            print(title)
        except:
            print('error')


