from selenium import webdriver
from bs4 import BeautifulSoup
import os
url = 'https://www.infinite-intelligence.net'
# Create a Firefox webdriver
driver = webdriver.Firefox()
# Open the website
driver.get(url)
# Execute JavaScript to get the entire HTML content inside the <body> tag
body_content = driver.execute_script("return document.body.outerHTML;")
# Close the webdriver
driver.quit()
# Parsing the HTML content using BeautifulSoup for easier manipulation
soup = BeautifulSoup(body_content, 'html.parser')
# Get all unique tags present in the body
unique_tags = set(tag.name for tag in soup.find_all())
# Create a directory to store individual HTML files
output_directory = 'output_tags_html'
os.makedirs(output_directory, exist_ok=True)
# Process each tag separately
for tag_name in unique_tags:
    # Extract HTML content for the specific tag
    tag_html = '\n'.join(str(item) for item in soup.find_all(tag_name))
    # Generate a unique filename using the tag name
    filename = f'{tag_name}_content.html'
    # Get the full file path
    html_file_path = os.path.join(output_directory, filename)
    # Write the tag-specific HTML content to the HTML file
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(tag_html)
    print(f'HTML content for tag "{tag_name}" saved to {html_file_path}')