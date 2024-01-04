import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def count_pages(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        internal_links = set()

        for link in soup.find_all('a', href=True):
            absolute_link = urljoin(url, link['href'])
            if absolute_link.startswith(url):  # Check if the link is within the same domain
                internal_links.add(absolute_link)

        return len(internal_links)
    else:
        print(f"Failed to fetch URL: {url}")
        return 0

# website_url = 'https://www.w3schools.com/'
# website_url = 'https://www.tutorialspoint.com'
website_url = 'https://www.infinite-intelligence.net/'
total_pages = count_pages(website_url)
print(f"Total pages on {website_url}: {total_pages}")
