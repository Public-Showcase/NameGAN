from bs4 import BeautifulSoup
import requests
import asyncio
from tqdm import tqdm

# modules imports
from getNameIds import getNameIds
from getData import getActorData
from saveData import saveData

# URL variables
base_url = ENV('BASE_URL')
# route = '/search/name/?gender=male&start=9950' # last link of `start` parameter, after this link will use `after` parameter
# route = '/search/name/?gender=male&start=1'

route = '/search/name/?gender=female&after=WzQ3MjAxLCJubTQ3MT%3D%3D'

async def scrapeActorsData(nameIds):
    tasks = [getActorData(nameId, 'f') for nameId in nameIds]
    results = []
    with tqdm(total=len(nameIds), desc="Scraping actors' data") as pbar:
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)
            pbar.update(1)
    return results

def abstractedDataSaver():
    global route

    # print('🕝 Getting data from', route, '...')

    response = requests.get(base_url + route) # getting HTML content
    soup = BeautifulSoup(response.content, 'html.parser') # parsing HTML content
    nameIds = getNameIds(listUrl=None, soup=soup) # getting nameIDs from HTML content
    
    asyncio.run(scrapeActorsData(nameIds))
    
    # print('✅ Completed saving data from', route, 'to CSV file.')

    try:
        next_list = soup.find('div', class_='desc').find_all('a')[-1]['href'] # getting next list link
        # print(next_list)
        
        if next_list:
            route = next_list
            abstractedDataSaver()
    except:
        next_list = None
        print('🛑 No more data to scrape. or something went wrong.')
        print("Last screpped list link: ", route)


abstractedDataSaver()
