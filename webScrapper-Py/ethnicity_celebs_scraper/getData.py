from bs4 import BeautifulSoup
import aiohttp
import asyncio

async def getData(link, isSave=True):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            try:
                full_name = soup.find('h1', class_='post-title').text.strip()
                first_name = full_name.split(' ')[0]
                last_name = full_name.split(' ')[-1]
            except:
                first_name = ''
                last_name = ''

            birth_country = ""
            birth_date = ""
            ethnicity = ""
            try:
                ps = soup.find('div', class_='entry').find('div', class_='entry-inner').find_all('p')
                # print(len(ps))

                for p in ps:
                    p = p.text.strip()
                    if "Place of Birth:" in p:
                        birth_country = p[p.find(':')+1:].split(',')[-1].strip()
                    elif "Date of Birth:" in p:
                        birth_date = p[p.find(':')+1:].replace(',', '')
                    elif "Ethnicity:" in p:
                        ethnicity = p[p.find(':')+1:].replace(',', ' &')
                
            except:
                print('## getData --> error getting data for', link)
                return {
                    "error": "error getting data!",
                    "link": link
                }
            
            # print(f'FirstName={first_name}, LastName={last_name}\nBirthPlace={birth_place}, BirthDate={birth_date}\nEthnicity={ethnicity}')

            data = f'{first_name}, {last_name}, {birth_date}, {birth_country}, {ethnicity}'.replace('\n', '') + '\n'

            if isSave:
                with open('celebData.csv', 'a') as file:
                    file.write(data)
            
            # returning for unit testing
            return data
        