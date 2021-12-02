import requests
from selenium import webdriver
import time
from tqdm import tqdm
import csv

browser = webdriver.Chrome()
url = "https://movie.naver.com/movie/point/af/list.nhn"
browser.get(url)

from tqdm import tqdm
reviewData = list()
# links = browser.find_element_by_class_name('paging').find_elements_by_tag_name('a')
_iter = 1000
for page in tqdm(range(_iter)):
    for row in browser.find_elements_by_tag_name('tr')[1:]:
        content = row.find_element_by_class_name('title').text.split('\n')
        title = content[0]
        point = content[2]
        text = content[3][:-4]
#         print(title, point, text)
        reviewData.append((title, point, text))
    browser.find_element_by_class_name('pg_next').click()



csvFile = open("./reviewData.csv", "a", newline="\n")
csvWriter = csv.writer(csvFile)

for row in reviewData:
    csvWriter.writerow(row)

csvFile.close()