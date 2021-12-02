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
# 1페이지에 20개 총 37페이지
# 영화 제목
# //*[@id="old_content"]/ul/li[1]/a
# //*[@id="old_content"]/ul/li[2]/a

# 2페이지
# //*[@id="old_content"]/ul/li[1]/a
# //*[@id="old_content"]/ul/li[2]/a

# //*[@id="movieEndTabMenu"]/li[6]/a/em
# //*[@id="reviewTab"]/div/div/div[2]/span/em 리뷰건수
# //*[@id="pagerTagAnchor2"]/span
# //*[@id="pagerTagAnchor10"]/em
# //*[@id="pagerTagAnchor2"]/em
# //*[@id="pagerTagAnchor3"]/em
# //*[@id="pagerTagAnchor1"]
# //*[@id="reviewTab"]/div/div/ul/li[1]/a/strong
# //*[@id="reviewTab"]/div/div/ul/li[2]/a/strong

# //*[@id="content"]/div[1]/div[4]/div[1]/div[4] user_tx_area


review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
try:
    for i in range(1, 38):
        url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page={}'.format(i)
        titles = []
        reviews = []
        for j in range(1, 21):
            print(j + ((i - 1) * 20), '번째 영화 크롤링 중')
            try:
                driver.get(url)
                movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
                title = driver.find_element_by_xpath(movie_title_xpath).text
                driver.find_element_by_xpath(movie_title_xpath).click()
                review_page_url = driver.find_element_by_xpath(review_button_xpath).get_attribute('href')
                driver.get(review_page_url)
                review_range = int(driver.find_element_by_xpath(review_number_xpath).text.replace(',', '')) // 10 + 2
                if review_range > 6: review_range = 6
                for k in range(1, review_range):
                    driver.get(review_page_url +'&page={}'.format(k))
                    for l in range(1, 11):
                        review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a/strong'.format(l)
                        try:
                            driver.find_element_by_xpath(review_title_xpath).click()
                            review = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
                            titles.append(title)
                            reviews.append(review)
                            driver.back()
                        except:
                            break

            except:
                print('error')
        df_review_20 = pd.DataFrame({'title':titles, 'reviews':reviews})
        df_review_20.to_csv('./crawling_data/reviews_{}_{}.csv'.format(2020, i), index=False)

except:
    print('totally error')
finally:
    driver.close()

# 연습