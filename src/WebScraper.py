from langchain_community.document_loaders import WebBaseLoader
from tqdm import tqdm

def extract_urls(records):
    """
        Params:
            --records: Dictionary representing the project's Airtable base

        Return:
            --urls: List of URLs to be scrapped             
    """
    urls = list()
    
    for record in records:
        id = record["id"]
        fields = record["fields"]
        if fields["UCSD?"] == 'no':
            if "Link" in fields.keys(): urls.append((fields["Link"], id))        
    
    return urls


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
    
    i = 0
    for document in tqdm(loader.lazy_load(), 
                         desc="Scraping data",
                         total=len(url), 
                         ncols=100,
                         unit="resource",
                         colour="#35e48f"):
        scrapped_text.append((document.page_content, id[i]))
        i += 1
    
    print()
    return scrapped_text
    