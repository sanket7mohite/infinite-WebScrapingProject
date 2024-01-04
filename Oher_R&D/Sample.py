import csv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver


url = 'https://www.tutorialspoint.com'
# url = 'https://www.infinite-intelligence.net'

response = requests.get(url)

if response.status_code == 200:

    with open('Data/scraped_content.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
        print("Content has been written to 'scraped_content.html'")
else:
    print("Failed to retrieve the content")

with open("scraped_content.html", "r") as f:
    html_doc = f.read()
soup = BeautifulSoup(html_doc, 'html.parser')

# print(soup.prettify())
# print('Title:-', soup.title.string)
#######################################################################################
########################### Downloading the Images from the Page #####################
#######################################################################################

imgs = soup.find_all('img')
imgs = imgs[1:]
print(imgs)

for img in imgs:
    # print(img)
    img_url = img.get('src')
    #
    img_name = os.path.basename(img_url)
    #     # print(img_name)
    #     # print(image)
    path = url + img_url
    # print(path)
    if path:
        # scode = img_response.status_code
        # print(f"status Code-> {scode}")
        # print(scode)
        actual_url = path
        parsed_url = urlparse(actual_url)
        corrected_netloc = parsed_url.netloc.replace('..', '.')
        path = f"{parsed_url.scheme}://{corrected_netloc}{parsed_url.path}"
        print(path)

    img_response = requests.get(path)
    if img_response.status_code == 200:
        print(f"URL is OK: {path}")
        img_name = os.path.join('downloaded_images', os.path.join(os.path.basename(path)))
        with open(img_name, 'wb') as img_file:
            img_file.write(img_response.content)
        print(f"Downloaded: {img_name}")
    else:
        print(f"Something is wrong with image URL: {path}")

#######################################################################################
########################### Parsing the Text from the Page ############################
#######################################################################################

html_content = response.content

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the text on the webpage
all_text = soup.get_text(separator='\n', strip=True)

# Split the text into lines
lines = all_text.split('\n')

# Define the CSV file name to save the data
csv_filename = os.path.join('WebSite_Text', 'webpage_data.csv')

# Write the text data into a CSV file
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    for line in lines:
        if line.strip():  # Write non-empty lines to the CSV file
            csv_writer.writerow([line])


#######################################################################################
########################### Taking Full Page ScreenShot ###############################
#######################################################################################
driver = webdriver.Firefox()
driver.get(url)
driver.save_full_page_screenshot('ScreenShots/ScreenShot.png')
driver.close()
