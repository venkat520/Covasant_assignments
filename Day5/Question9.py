# Given a URL, download that and parse 
# and download all links inside that page 
    # Use ThreadPoolExecutor or ProcessPoolExecutor 
    # BeautifulSoup for parsing html, requests for downloading
    
    
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

def fetch(url):
    try:
        response=requests.get(url, timeout=5)
        print(f"Downloaded:{url}")
        return url,response.text
    except:
        print(f"Failed to Download:{url}")
        return url,None
        
def get_links(base_url,html):
    soup=BeautifulSoup(html,'html.parser')
    return [urljoin(base_url,a['href']) for a in soup.find_all('a',href=True)]
    
def main(url):
    base_url,html=fetch(url)
    if not html:
        return
        
    links=get_links(base_url,html)
    
    with ThreadPoolExecutor() as executor:
        executor.map(fetch,links)
        
        
if __name__=='__main__':
    main("https://amazon.com")