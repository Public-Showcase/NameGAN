from bs4 import BeautifulSoup
import requests

def getNameIds(listUrl=None, soup=None):
    
    if listUrl:
        response = requests.get(listUrl)
        soup = BeautifulSoup(response.content, 'html.parser')
    
    nameIds = []

    for div in soup.find_all('div', class_='lister-item mode-detail'):
        link = div.find('div', class_='lister-item-content').find('h3').find('a')['href']
        if(link):
            nameIds.append(link.split('/')[-1])

    # print(len(nameIds), nameIds)

    return nameIds
