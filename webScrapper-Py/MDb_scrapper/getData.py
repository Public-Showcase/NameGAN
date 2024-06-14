__all__ = ['getActorData'] # exporting for testing

from bs4 import BeautifulSoup
import aiohttp
import asyncio


def get_first_last_name(name):
    # removing symbols form the name
    name = name.replace('(', '')
    name = name.replace(')', '')
    name = name.replace('.', '')
    name = name.replace(',', '')

    # Split the name string into parts based on whitespace
    parts = name.split()

    # Get the first and last name
    first_name = parts[0]
    last_name = parts[-1]

    # Return the first and last name as a tuple
    return (first_name, last_name)

async def getActorData(nameID, gender, isSave=True):
    url = f'{ENV("BASE_URL")}/name/{nameID}/bio'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # name
            first_name = ""
            last_name = ""
            try:
                full_name = soup.find('h3').text.strip().split(' ')
                # full_name = soup.find('div', class_='parent').find('h3').text.strip().split(' ')
                if full_name and len(full_name) >= 2: # for people with fist and last name and middle name
                    first_name = full_name[0]
                    last_name = full_name[1]
                elif full_name and len(full_name) == 1: # for people with only first name
                    first_name = full_name[0]

            except:
                # print("Couldn't find name.")
                pass

            # birth_date
            birth_date = None

            try:
                temp = soup.find('time')
                birth_date = temp['datetime']
                # print(birth_date)
            except:
                # print("Couldn't find birth date.")
                pass

            # birth_place
            birth_place_state = None
            birth_place_country = None

            try:
                birth_place = soup.find('time').find_next_sibling('a').text.strip().split(',')
                if birth_place and len(birth_place) >= 2:
                    birth_place_state = birth_place[-2]
                    birth_place_country = birth_place[-1]
                # print(birth_place_country, birth_place_state)
            except:
                # print("Couldn't find birth place.")
                pass

            # parents name
            mother_first_name = ""
            mother_last_name = ""
            father_first_name = ""
            father_last_name = ""

            try:
                parents_name = soup.find('table', id='tableFamily').findAll('tr')
                for tr in parents_name:
                    if 'Parents' in tr.text:
                        parents_name = tr.find('td').next_sibling.next_sibling.text.strip().split(' ')
                        parents_name = list(filter(lambda x: not not x and not x == "\n", parents_name))

                        # print(parents_name)

                        temp_name = ""
                        for n in parents_name:
                            temp_name += n + " "
                        temp_name = temp_name.split("\n")

                        # print(temp_name)

                        mother_first_name, mother_last_name = get_first_last_name(temp_name[0])
                        father_first_name, father_last_name = get_first_last_name(temp_name[1])
                        
                        break
                                
                # print(mother_first_name, mother_last_name, father_first_name, father_last_name)
            except:
                # print("Couldn't find parents name.")
                pass

            data = f"{first_name},{last_name},{birth_date},{birth_place_state},{birth_place_country},{mother_first_name},{mother_last_name},{father_first_name},{father_last_name},{gender},None\n"
        
            if isSave:
                with open('actorsData.csv', 'a') as file:
                    file.write(data)
            
            # returning for unit testing
            return { 
                'first_name': first_name,
                'last_name': last_name,
                'birth_date': birth_date,
                'birth_place_state': birth_place_state,
                'birth_place_country': birth_place_country,
                'mother_first_name': mother_first_name,
                'mother_last_name': mother_last_name,
                'father_first_name': father_first_name,
                'father_last_name': father_last_name,
                'gender': gender,
                'ethnicity': 'None'
            }

# for testing
# async def main():
#     # res = await getActorData('nm0647634', 'f', isSave=False)
#     # res = await getActorData('nm3009232', 'm', isSave=False)
#     # res = await getActorData('nm0241049', 'm', isSave=False)
#     res = await getActorData('nm0451307', 'm', isSave=False)
    
#     print(res)

# asyncio.run(main())
