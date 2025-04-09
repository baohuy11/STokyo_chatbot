import os
import re
import json
import time
import string
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Set a global user agent for requests
USER_AGENT = UserAgent().chrome
os.environ['USER_AGENT'] = USER_AGENT

def clean_text(text: str) -> str:
    """
    Remove non-alphabetic characters from the text.
    
    :param text: Input string.
    :return: Cleaned string.
    """
    return re.sub(r'[^a-zA-Z\s]', ' ', text).strip()

def extract_disease_links(url: str) -> dict:
    """
    Fetch the a-to-z page and extract disease links.
    
    :param url: URL of the a-to-z listing page.
    :return: Dictionary mapping disease names to full URLs.
    """
    headers = {"User-Agent": os.environ.get('USER_AGENT', "Mozilla/5.0")}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    disease_links = {}
    
    for letter in string.ascii_lowercase:
        class_name = f"az_list_indivisual {letter}_detail"
        div = soup.find("div", class_=class_name)
        if not div:
            continue
        for link in div.find_all("a"):
            # Clean and normalize disease name
            name = clean_text(link.get_text(strip=True))
            href = link.get("href", "")
            full_url = urljoin(url, href)
            disease_links[name] = full_url
    return disease_links

def extract_text_from_page(url: str) -> str:
    """
    Retrieve and extract all paragraph text from a given page URL.
    
    :param url: URL of the disease page.
    :return: Extracted text content.
    """
    # Polite delay before making the request
    time.sleep(2)
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all("p")
    return "\n".join(p.get_text(strip=True) for p in paragraphs)

def extract_main_content(soup: BeautifulSoup) -> str:
    """
    Extract the main content from a BeautifulSoup object by removing non-content elements.
    
    :param soup: BeautifulSoup object of a page.
    :return: Concatenated text of content-related tags.
    """
    main = soup.find('div', id='main')
    if not main:
        return ""
    
    # Remove unwanted elements by their class names
    for cls in ['boxContact02', 'contact', 'footer', 'nav', 'sidebar']:
        for el in main.find_all(class_=cls):
            el.decompose()
    
    content_tags = main.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'article', 'section'])
    return ' '.join(tag.get_text(separator=' ', strip=True) for tag in content_tags)

def save_data_locally(data: dict, filename: str, directory: str) -> None:
    """
    Save data as a JSON file to the specified directory.
    
    :param data: Data dictionary to save.
    :param filename: Name of the file (e.g. 'symptom.json').
    :param directory: Directory path to save the file.
    """
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {file_path}")

def main() -> None:
    base_url = "https://www.nhsinform.scot/illnesses-and-conditions/a-to-z/"
    diseases = extract_disease_links(base_url)
    
    disease_data = {}
    for name, link in diseases.items():
        print(f"Fetching content for {name}...")
        content = extract_text_from_page(link)
        disease_data[name] = {"url": link, "content": content}
    
    save_data_locally(disease_data, "symptom.json", "data")

if __name__ == '__main__':
    main()
