from bs4 import BeautifulSoup
import aiohttp
import asyncio

MAIN_URL = ENV("MAIN_URL")

async def getLinks(isSave=True):
    """
    needs to use async, since normal requests will give unauthorized error

    this returns a list of links to the pages of each celebrities, this also included links for the category pages which can be filtered out later
    there is option to save the links to a csv file, which can be used to get the data later
    """
    print("Getting links...")
    async with aiohttp.ClientSession() as session:
        async with session.get(MAIN_URL) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            listItems = soup.find('ul', class_='wsp-posts-list').find_all('li')
            
            links = [li.find('a')['href'] for li in listItems]
            print(len(links))
            print(links[0])
            print(links[1])

            if isSave:
                with open('links.csv', 'w') as file:
                    file.write("\n".join(links))
                    file.close()
                    print("## getLinks --> Saved links to links.csv")
            
            print("## getLinks --> Done getting links")
            return links

# for testing only
# async def main():
#     # res = await getLinks(isSave=False)
#     res = await getLinks()
#     print(res)

# asyncio.run(main())
