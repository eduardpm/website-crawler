from bs4 import BeautifulSoup
import requests


def crawl_website(url, parser):
    headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com",
}
    # Send a GET request to the website
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup``
        soup = BeautifulSoup(response.content, 'html.parser')
                
        parser(soup)
    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

    return True if response.status_code == 200 else False