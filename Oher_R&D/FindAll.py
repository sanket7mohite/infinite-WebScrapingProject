import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to get all pages from a website
def find_all_pages(url):
    # Set up empty set to store unique URLs
    all_pages = set()
    # Add the initial URL to the set
    all_pages.add(url)

    # Function to parse a page and extract all links
    def parse_page(page_url):
        try:
            response = requests.get(page_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link.get('href')
                    # Join the URL if it's relative
                    full_url = urljoin(page_url, href)
                    # Check if it's a valid URL of the same domain
                    if full_url.startswith(url) and full_url not in all_pages:
                        all_pages.add(full_url)
                        # Recursive call to parse new pages
                        parse_page(full_url)
        except requests.RequestException as e:
            print(f"Error: {e}")

    # Start parsing from the initial URL
    parse_page(url)

    return all_pages

website_url = 'https://www.w3schools.com/'
# website_url = 'https://www.tutorialspoint.com'
# website_url = 'https://www.infinite-intelligence.net/'
pages = find_all_pages(website_url)

# Print all found pages
for page in pages:
    print('test')
    print(page)
