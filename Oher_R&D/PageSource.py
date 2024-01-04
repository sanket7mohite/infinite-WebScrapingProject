from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
url = 'https://www.infinite-intelligence.net'
driver.get(url)

# Extract meta description
# meta_description = driver.find_element_by_css_selector('meta[name="description"]').get_attribute('content')
meta_description = driver.find_element(By.XPATH, "//meta[@name='description']").get_attribute('content')
print(meta_description)
# Extract meta viewport
# meta_viewport = driver.find_element_by_css_selector('meta[name="viewport"]').get_attribute('content')
meta_viewport = driver.find_element(By.XPATH, "//meta[@name='viewport']").get_attribute('content')
print(meta_viewport)
