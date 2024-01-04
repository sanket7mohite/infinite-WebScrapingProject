from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
url = 'https://www.infinite-intelligence.net'
driver.get(url)
driver.save_full_page_screenshot('Selenium_ScreenShots/ScreenShot.png')
driver.close()
