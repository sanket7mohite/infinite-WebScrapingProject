import time
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://www.infinite-intelligence.net'

driver = webdriver.Firefox()
driver.get(url)

time.sleep(5)
body = driver.find_element(By.TAG_NAME, 'body').text
print(body)

# all_text = ' '.join(element.text for element in elements if element.text.strip())

# Save all text to a file or do further processing
with open('WebSite_Text/webpage_text.json', 'w', encoding='utf-8') as file:
    file.write(body)

driver.quit()
