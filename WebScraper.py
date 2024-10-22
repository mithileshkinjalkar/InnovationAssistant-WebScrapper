from langchain_community.document_loaders import WebBaseLoader
from tqdm import tqdm

# Function to extract URLs for each record in the Airtable
# The record ID is preserved for writing later
def extract_urls(records):
    """
        Params:
            --records: Dictionary representing the project's Airtable base

        Return:
            --urls: List of URLs to be scrapped             
    """
    urls = list()
    
    # Extracting the ID and URL if resource is a non-UCSD resource
    for record in records:
        id = record["id"]
        fields = record["fields"]
        if fields["UCSD?"] == 'no':
            if "Link" in fields.keys(): urls.append((fields["Link"], id))        
    
    return urls


# Function to crawl across all the extracted URLs and scrape text on them
def scrape_urls(urls):
    """
        Params:
            --urls: List of URLs to be scrapped

        Return:
            --scrapped_text: List of strings representing scrapped text from the provided URLs
     """
    scrapped_text = list()

    url, id = zip(*urls)
    loader = WebBaseLoader(url)
    
    # Lazy loading for iterative operation
    i = 0
    for document in tqdm(loader.lazy_load(), 
                         desc="Scraping data",
                         total=len(url), 
                         ncols=100,
                         unit="resource",
                         colour="#35e48f"):
        if "500" in document.metadata["title"] or\
            "502" in document.metadata["title"] or\
            "403" in document.metadata["title"] or\
            "404" in document.metadata["title"] or\
            "401" in document.metadata["title"] or\
            "410" in document.metadata["title"] or\
            "503" in document.metadata["title"] or\
            "504" in document.metadata["title"] or\
            "414" in document.metadata["title"] or\
            "408" in document.metadata["title"] or\
            "415" in document.metadata["title"] or\
            "Unpublished" in document.metadata["title"]: 
            i += 1
            continue
        scrapped_text.append((document.page_content, id[i]))
        i += 1
    
    print()
    return scrapped_text
    