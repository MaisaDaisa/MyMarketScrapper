import sqlite3

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from Post import Post
from PostDB import PostDB
import demoji
import time

database = PostDB('postdb.db')
start_url = str(input('Please Input the link of finished categories (keep in mind it must contain Page=1 at the end): '))

driver = webdriver.Chrome()

driver.implicitly_wait(30)
driver.get(start_url)
time.sleep(2)

close_ad = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[1]/button/i')
close_ad.click()


site_soup = BeautifulSoup(driver.page_source, 'html.parser')
pages = int(site_soup.find_all('a', {'class': 'pagination-link'})[-2].text.strip())
posts = site_soup.find_all('a', {'class': 'h-100 d-block text-decoration-none'})

for num_page in range(1, pages):

    url = start_url[:-1] + str(num_page)
    driver.get(url)
    time.sleep(0.5)

    def remove_emojis(text):
        return demoji.replace(text, '')

    for upload in posts:
        name = remove_emojis(upload.find('h4').text.strip())
        link = 'https://www.mymarket.ge' + upload['href']
        subscribtion = upload.div.div.text.strip()
        condition = upload.div.div.next_sibling.text.strip()
        page = num_page
        has_delivery = upload.find('span', {"class": 'font-size-11 font-size-md-12 font-base text-dark-green'}) is not None
        try:
            price = upload.find('span', {'class': 'text-black font-bold font-size-14 line-height-6'}).text.strip()
        except:
            price = None

        post = Post(name, price, condition, link, subscribtion, has_delivery, page)

        database.add_post(post)


driver.close()
