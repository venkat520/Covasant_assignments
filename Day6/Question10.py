
# Given a URL, download that and parse 
# and download all links inside that page 
    # in asyncio 
    # BeautifulSoup for parsing html, requests for downloading
    
    
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin

async def fetch(url,session):
    try:
        async with session.get(url) as response:
            print(f"Downloaded:{url}")
            return await response.text()
    except:
        print(f"Failed to download:{url}")
        return ""
        
async def main(url):
    async with aiohttp.ClientSession() as session:
        html=await fetch(url,session)
        soup=BeautifulSoup(html,'html.parser')
        links=[urljoin(url,a['href']) for a in soup.find_all('a',href=True)]
        
        tasks=[fetch(link,session) for link in links[:10]]
        await asyncio.gather(*tasks)
        
        
if __name__=='__main__':
    asyncio.run(main("https://amazon.com"))