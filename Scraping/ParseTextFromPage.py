import csv
import os

import requests
from bs4 import BeautifulSoup

url = 'https://www.infinite-intelligence.net'

response = requests.get(url)
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
csv_filename = os.path.join('PageText', 'webpage_data.csv')

# Write the text data into a CSV file
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    for line in lines:
        if line.strip():  # Write non-empty lines to the CSV file
            csv_writer.writerow([line])
