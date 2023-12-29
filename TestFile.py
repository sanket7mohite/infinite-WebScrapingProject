import csv
import os
from builtins import print
from itertools import zip_longest

from WebScraper import WebScraper

# Usage:
scraper = WebScraper()
scraper.createFolder()
output_dir = os.getenv('PageName')
DOM = scraper.scrape_page_source(scraper.driver, output_dir)
soup = scraper.soup_dom(DOM)

image_names_img_tag = []
image_names_img_tag = scraper.download_images_from_img_tag(output_dir)

image_names_css = []
image_names_css = scraper.download_images_from_css(output_dir)

all_img_tag = []
all_img_tag = scraper.get_img_tag(soup)


# Function to get page title
page_title = scraper.get_page_title(soup)

# Function to get the all script tags
all_script_tag = []
all_script_tag = scraper.get_script_tag(soup)

# Function to get the all meta tags
all_meta_tag = []
all_meta_tag = scraper.get_meta_tag(soup)

# Function to get the all anchor tags
all_anchor_tag = []
all_anchor_tag = scraper.get_anchor_tag(soup)

# Function to get the all link tags
all_link_tag = []
all_link_tag = scraper.get_link_tag(soup)

# Function to get the Google script manager content
google_script_content = scraper.get_google_script_content(soup)

fieldnames = ['page_title', 'meta_tag', 'Scripts_tag', 'anchor_tag', 'link_tag', 'img_names_from_img_tag', 'img_names_from_css', 'images_tag']
csv_filename = 'WebScraping.csv'

# Adding page_title, all_meta_tag, all_script_tag, all_anchor_tag, all_link_tag, image_names_img_tag, image_names_css, all_img_tag into CSV file
scraper.write_to_csv(page_title, all_meta_tag, all_script_tag, all_anchor_tag, all_link_tag, image_names_img_tag, image_names_css, all_img_tag, output_dir,  'WebScraping.csv')

# Appending the column 'google-tag-manger' into csv file
scraper.create_or_append_csv('google-tag-manger', google_script_content, output_dir,  'WebScraping.csv')

