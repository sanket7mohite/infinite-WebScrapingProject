import csv
import os
import time
from typing import Dict
from urllib.parse import urlparse

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://www.infinite-intelligence.net'

driver = webdriver.Firefox()
driver.get(url)


########################### Scrape Head ContentScrape Head ContentScrape Head ContentScrape Head Content ############################
page_head = driver.find_element(By.TAG_NAME, 'head')
head_content = page_head.get_attribute('innerHTML')
print(head_content)


print('########################### Scrape Body Content ############################')
########################### Scrape Body Content ############################
page_body_HTML = driver.find_element(By.TAG_NAME, 'body')
body_content = page_body_HTML.get_attribute('innerHTML')
print(body_content)

########################### Scrape Body Text Content ############################
print('########################### Scrape Body Text Content ############################')
body_text = page_body_HTML.get_attribute('innerText')
# print(body_text)

########################### Scrape Achor and Links Tags ############################
'''
print('########################### Scrape Body Text Content ############################')
# page_links = []
page_links = driver.find_elements(By.TAG_NAME, 'a')
links = page_body_HTML.get_attribute('href')
print(links)
# for link in links:
#     print(link)

'''



driver.quit()

'''
meta_description = driver.find_element(By.XPATH, "//meta[@name='description']").get_attribute('content')
print(meta_description)
meta_viewport = driver.find_element(By.XPATH, "//meta[@name='viewport']").get_attribute('content')
print(meta_viewport)
'''