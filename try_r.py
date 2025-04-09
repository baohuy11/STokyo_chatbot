import requests
from fake_useragent import UserAgent
from urllib.parse import urljoin
import time
from bs4 import BeautifulSoup

USER_AGENT = UserAgent().chrome
headers = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    # Sometimes removing or changing the Referer can help
    "Accept-Language": "en-US,en;q=0.9",
}

def extract_text_from_page(url: str) -> str:
    time.sleep(2)
    with requests.Session() as session:
        session.headers.update(headers)
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all("p")
        return "\n".join(p.get_text(strip=True) for p in paragraphs)

# Test on the problematic URL:
url = "https://www.nhsinform.scot/illnesses-and-conditions/infections-and-poisoning/coronavirus-covid-19/coronavirus-covid-19/"
print(extract_text_from_page(url))
