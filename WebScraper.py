import csv
import json
import os
import time
from itertools import zip_longest
from typing import Dict
from urllib.parse import urlparse
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from dotenv import load_dotenv, dotenv_values
from openpyxl import Workbook


class WebScraper:
    def __init__(self):
        load_dotenv()
        self.driver = webdriver.Firefox()
        self.driver.get(os.getenv('url'))

    def createFolder(self):
        output_directory = os.getenv('PageName')
        os.makedirs(output_directory, exist_ok=True)

    def scrape_page_source(self, driver, output_directory):
        time.sleep(5)
        file_path = os.path.join(output_directory, 'Page_Source.html')
        DOM = driver.page_source
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(DOM)
            return DOM

    def soup_dom(self, DOM):
        soup = BeautifulSoup(DOM, 'html.parser')
        return soup

    def get_page_title(self, soup):
        page_title = soup.find('title')
        return page_title

    def get_body_tag(self, soup):
        body_tag = soup.find('body')
        return body_tag

    def get_anchor_tag(self, soup):
        anchor_tag = soup.find_all('a')
        return anchor_tag

    def get_link_tag(self, soup):
        link_tag = soup.find_all('link')
        return link_tag

    def get_script_tag(self, soup):
        script_tag = soup.find_all('script')
        return script_tag

    def get_meta_tag(self, soup):
        meta_tag = soup.find_all('meta')
        return meta_tag

    def get_img_tag(self, soup):
        img_tag = soup.find_all('img')
        return img_tag

    def get_body_text(self, soup, filepath):
        output_dir = os.path.join(filepath)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        body_tag = soup.find('body')  # Find the <body> tag
        if body_tag:
            body_text = body_tag.get_text(separator='\n', strip=True)  # Extract text content within <body>

            # Write body text to a file
            file_path = os.path.join(output_dir, 'body_text.txt')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(body_text)

    def save_google_script_content_csv(self, soup):
        google_script_content = soup.find(id='ao-CookiePolicy')['data-pc']
        file_name = 'google_script_content.csv'
        with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Google Tag Manager Script Content'])
            writer.writerow([google_script_content])

    def get_google_script_content(self, soup):
        google_script_content = soup.find(id='ao-CookiePolicy')['data-pc']
        return google_script_content

    def create_or_append_csv(self, header, data, filepath, csv_filename):
        # csv_filename = 'WebScraping.csv'
        # Create the directory if it doesn't exist
        output_dir = os.path.join(filepath)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            # Check if the file exists
        if os.path.exists(csv_filename):
            csv_filename = os.path.join(output_dir, csv_filename)
            df = pd.read_csv(csv_filename)
            if header not in df.columns:
                # If the header doesn't exist, create a new column and add data to the first row
                df[header] = ''
                df.at[0, header] = data
                df.to_csv(csv_filename, index=False)
            else:
                # If the header exists, update the first row with the new data
                df.at[0, header] = data
                df.to_csv(csv_filename, index=False)
        else:
            # If the file doesn't exist, create a new file and add header and data
            df = pd.DataFrame({header: [data]})
            df.to_csv(csv_filename, index=False)

    # Function to create or append to CSV file with dynamic headers
    def create_csv_Template(self, file_path, headers, data):

        csv_filename = 'WebScraping.csv'
        if os.path.exists(csv_filename):
            df = pd.read_csv(csv_filename)
            # Add new data to existing columns or create new columns if not present
            for col, val in zip(headers, data):
                df[col] = val
            df.to_csv(csv_filename, index=False)
        else:
            # Create a new DataFrame with headers and data and save to CSV
            df = pd.DataFrame({col: [val] for col, val in zip(headers, data)})
            df.to_csv(csv_filename, index=False)

    def download_images_from_img_tag(self, filepath):
        image_data = []
        image_elements = self.driver.find_elements(By.TAG_NAME, "img")

        # Create the directory if it doesn't exist
        output_dir = os.path.join(filepath, 'Images_from_img_tag')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for idx, img in enumerate(image_elements):
            img_url = img.get_attribute('src')
            if img_url:
                actual_url = img_url
                parsed_url = urlparse(actual_url)
                corrected_netloc = parsed_url.netloc.replace('..', '.')
                path = f"{parsed_url.scheme}://{corrected_netloc}{parsed_url.path}"

                img_response = requests.get(path)
                if img_response.status_code == 200:
                    file_name = os.path.basename(path)
                    img_name = os.path.join(output_dir, file_name)
                    image_data.append(file_name)
                    with open(img_name, 'wb') as img_file:
                        img_file.write(img_response.content)
                    print(f"Downloaded: {img_name}")
                else:
                    print(f"Something is wrong with image URL: {path}")

        return image_data

    def download_images_from_css(self, filepath):
        image_data = []
        ele_list = self.driver.find_elements(By.TAG_NAME, "div")

        # Create the directory if it doesn't exist
        output_dir = os.path.join(filepath, 'Images_from_css')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for ele in ele_list:
            img_path = ele.value_of_css_property('background-image')

            if 'https' in img_path:
                path = img_path.split('url("')[1].split('")')[0]
                if path:
                    actual_url = path
                    parsed_url = urlparse(actual_url)
                    corrected_netloc = parsed_url.netloc.replace('..', '.')
                    path = f"{parsed_url.scheme}://{corrected_netloc}{parsed_url.path}"

                img_response = requests.get(path)
                if img_response.status_code == 200:
                    # img_name = os.path.join('Selenium_Downloaded_Images', os.path.basename(path))
                    file_name = os.path.basename(path)
                    img_name = os.path.join(output_dir, file_name)
                    image_data.append(file_name)
                    # image_data.append({'Image_FileName': file_name})
                    with open(img_name, 'wb') as img_file:
                        img_file.write(img_response.content)
                    print(f"Downloaded: {img_name}")
                else:
                    print(f"Something is wrong with image URL: {path}")

        return image_data

    def scrape_meta_data(self):
        meta_description = self.driver.find_element(By.XPATH, "//meta[@name='description']").get_attribute('content')
        meta_viewport = self.driver.find_element(By.XPATH, "//meta[@name='viewport']").get_attribute('content')

        return {'meta_description': meta_description, 'meta_viewport': meta_viewport}

    def save_to_csv(self, image_data, meta_data):
        fieldnames = ['Image_FileName', 'meta_description', 'meta_viewport']
        csv_filename = 'WebScraping.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Image_FileName': image_data, 'meta_description': meta_data['meta_description'],
                             'meta_viewport': meta_data['meta_viewport']})

    def fullPage_page_screnshot(self, driver, filepath):
        filename = 'FullPageScreenShot.png'
        output_dir = os.path.join(filepath)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            if os.path.exists(filename):
                screenshot_filename = os.path.join(output_dir,filename)
        file_path = os.path.join('output_directory', 'screenshot_filename')

    def quiteBrowser(self, driver):
        self.driver.quit()

    def write_to_csv(self, page_title, all_meta_tag, all_script_tag, all_anchor_tag, all_link_tag, image_names_img_tag,
                     image_names_css, all_img_tag, filepath, csv_filename):

        # Create the directory if it doesn't exist
        output_dir = os.path.join(filepath)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            # Check if the file exists
        if os.path.exists(csv_filename):
            csv_filename = os.path.join(output_dir, csv_filename)

            fieldnames = ['page_title', 'meta_tag', 'Scripts_tag', 'anchor_tag', 'link_tag', 'img_names_from_img_tag',
                          'img_names_from_css', 'images_tag']

            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for title, meta_tag, script_tag, anchor_tag, link_tag, names_img_tag, names_css_tag, images_tag in zip_longest(
                        page_title, all_meta_tag, all_script_tag, all_anchor_tag, all_link_tag, image_names_img_tag,
                        image_names_css, all_img_tag, fillvalue=''):
                    writer.writerow({
                        'page_title': title,
                        'meta_tag': meta_tag,
                        'Scripts_tag': script_tag,
                        'anchor_tag': anchor_tag,
                        'link_tag': link_tag,
                        'img_names_from_img_tag': names_img_tag,
                        'img_names_from_css': names_css_tag,
                        'images_tag': images_tag
                    })

    def login(self, driver):
        url = os.getenv('url')
        login_url = url + '/login'
        self.driver.get(login_url)
        self.driver.find_element(By.XPATH, "//input[@id='aoLogin-email']").send_keys(os.getenv('email'))
        self.driver.find_element(By.XPATH, "//input[@id='aoLogin-password']").send_keys(os.getenv('password'))
        self.driver.find_element(By.XPATH, "//button[@id='aoLogin-Login']").click()

    def navigateMenu_Technologies(self, driver):
        ele = self.driver.find_element(By.XPATH, "//a[@title='Technologies']/parent::div[@class='aos__menu__node']")
        self.move_to_element(self.driver, ele)

    def move_to_element(self, driver, element):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()


    def get_blog_title(self, driver):
        blog_title = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'ArticleTitle')]").text
        return blog_title

    def get_blog_category(self, driver):
        blog_category = self.driver.find_element(By.XPATH, "//a[contains(@class, 'ataCategory')]").text
        return blog_category

    def get_blog_date(self, driver):
        blog_date = self.driver.find_element(By.XPATH, "//span[contains(@class, 'ArticleDate')]").text
        return blog_date

    def get_blog_author(self, driver):
        blog_author = self.driver.find_element(By.XPATH, "//span[contains(@class, 'ArticleAuthor')]").text
        return blog_author

    def get_blog_articleAccount(self, driver):
        blog_articleAccount = self.driver.find_element(By.XPATH, "//span[contains(@class, 'ArticleAccount')]").text
        return blog_articleAccount

    def get_blog_intro(self, driver):
        blog_intro = self.driver.find_element(By.XPATH, "//div[contains(@class, 'IntroText')]").text
        return blog_intro

    def get_blog_description(self, driver):
        blog_description = self.driver.find_element(By.XPATH, "//div[contains(@class, 'Teaser')]").text
        return blog_description

    def get_blog_context(self, driver):
        blog_context = self.driver.find_element(By.XPATH, "//div[contains(@class, 'ShareLinks')]/following::div[1]").text
        return blog_context

    # Title 	Blog Category	Blog Date	Blog Author Source	Blog Short Description	Blog Content
    def write_to_csv_blog(self, blog_title, blog_category, blog_date, blog_author, blog_articleAccount, blog_intro, blog_context, filepath, csv_filename):

        # Create the directory if it doesn't exist
        output_dir = os.path.join(filepath)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            # Check if the file exists
        if os.path.exists(csv_filename):
            csv_filename = os.path.join(output_dir, csv_filename)

            fieldnames = ['blog_title', 'blog_category', 'blog_date', 'blog_author', 'blog_articleAccount', 'blog_intro',
                          'blog_context']

            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for title, category, date, author, articleAccount, intro, context in zip_longest(
                        blog_title, blog_category, blog_date, blog_author, blog_articleAccount, blog_intro, blog_context, fillvalue=''):
                    writer.writerow({
                        'blog_title': title,
                        'blog_category': category,
                        'blog_date': date,
                        'blog_author': author,
                        'blog_articleAccount': articleAccount,
                        'blog_intro': intro,
                        'blog_context': context
                    })
