import os
import re
import json
from langchain_community.document_loaders import RecursiveUrlLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from fake_useragent import UserAgent

os.environ['USER_AGENT'] = UserAgent().chrome

load_dotenv()
def bs4_extractor(html: str) -> str:
    """
    Function to extract and clean content from HTML
    Args: 
        html: HTML string to be processed 
    Returns: 
        str: Text has been cleaned, removing HTML tags and extra spaces
    """
    soup = BeautifulSoup(html, "html.parser") # Parse HTML
    return re.sub(r"\n\n+", "\n\n", soup.texr).strip() # Remove extra spaces and blank lines

def crawl_web(url_data):
    """
    Function to crawl data from URL with recursive mode 
    Args: 
        url_data (str): Original URL to start crawling 
    Returns: 
        list: List of Document objects, each object contains divided content 
            and corresponding metadata
    """
    # Create a loader with a maximum depth of 4 levels
    loader = RecursiveUrlLoader(url = url_data, extractor = bs4_extractor, max_depth = 4)
    docs = loader.load() # Download content
    print('length: ', len(docs)) # Print the number of loaded documents

    # Split text into 10000 character chunks, with 500 character overlaps
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 500)
    all_splits = text_splitter.split_documents(docs)
    print('length_all_splits: ', len(all_splits)) # Print the number of text paragraphs after dividing
    return all_splits

def web_base_loader(url_data):
    """
    Function to load data from a single URL (not recursive) 
    Args: 
        url_data (str): URL to download data 
    Returns: 
        list: List of Document objects that have been broken down
    """
    loader = WebBaseLoader(url_data) # Create basic loader
    docs = loader.load() # Download the content
    print('length: ', len(docs)) # Print the number of the document

    # Split the document same as above
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 500)
    all_split = text_splitter.split_documents(docs)
    return all_split

def save_data_locally(documents, filename, directory):
    """
    Save a list of documents to a JSON file 
    Args: 
        documents (list): List of Document objects to save 
        filename (str): JSON file name (for example: 'data.json')
        directory (str): Directory path to save the file 
    Returns:
        None: The function does not return a value, only saves the file and prints a message
    """
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename) # Generate full path

    # Convert documents into serializable format
    data_to_save = [{'page_content': doc.page_content, 'metadata': doc.metadata} for doc in documents]
    # Save to JSON file
    with open(file_path, 'w') as file:
        json.dump(data_to_save, file, indent = 4)
        print(f'Data saved to {file_path}') # Print a successful save message

#def main():
    """
    The main function controls the program flow: 
    1. Crawl data from stack-ai website 
    2. Save crawled data to JSON file 
    3. Print crawl results for checking
    """
    # Crawl data from stack-ai docs page
    #data = crawl_web('https://www.stack-ai.com/docs')
    # Save data to data_v2 folder
    #save_data_locally(data, 'stack.json', 'data')
    #print('data: ',data) # Print crawled data

# Check if the file is run directly
#if __name__ == "__main__":
    #main()