import csv
import os
from builtins import print
from itertools import zip_longest

from dotenv import load_dotenv

from WebScraper import WebScraper

# Usage:
scraper = WebScraper()
scraper.createFolder()
output_dir = os.getenv('PageName')
DOM = scraper.scrape_page_source(scraper.driver, output_dir)
soup = scraper.soup_dom(DOM)

blogtitle = scraper.get_blog_title(scraper.driver)
# print('blogtitle->', blogtitle)

blogcategory = scraper.get_blog_category(scraper.driver)

blogdate = scraper.get_blog_date(scraper.driver)

blogauthor = scraper.get_blog_author(scraper.driver)

blogarticleAccount = scraper.get_blog_articleAccount(scraper.driver)

blogintro = scraper.get_blog_intro(scraper.driver)

# blogdescription = scraper.get_blog_description(scraper.driver)

blogcontext= scraper.get_blog_context(scraper.driver)

# print(blog_context)
scraper.fullPage_page_screnshot(scraper.driver, output_dir)

'''
load_dotenv()
if 'articles' in os.getenv('url'):


    # Title 	Blog Category	Blog Date	Blog Author Source	Blog Short Description	Blog Content
    fieldnames = ['blog_title', 'blog_category', 'blog_date', 'blog_author', 'blog_articleAccount', 'blog_Teaser', 'blog_context']
    csv_filename = 'WebScraping_blog.csv'

    # Adding page_title, all_meta_tag, all_script_tag, all_anchor_tag, all_link_tag, image_names_img_tag, image_names_css, all_img_tag into CSV file
    scraper.write_to_csv_blog(blogtitle, blogcategory, blogdate, blogauthor, blogarticleAccount, blogintro,
                          blogcontext, 'output_dir', 'csv_filename')

    scraper.quiteBrowser(scraper.driver)
'''