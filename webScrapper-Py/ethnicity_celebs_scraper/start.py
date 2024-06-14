from getLinks import getLinks
from getData import getData
import asyncio
from tqdm import tqdm
from datetime import datetime
 
dt_string = datetime.now().strftime("%d-%m-%Y %H-%M")
saveFile = f'celebData_{dt_string}.csv'

async def main():
    # get links
    # links = await getLinks(isSave=False)
    # print("Fetching links...")

    # user prefetched links from links.csv
    with open('links.csv', 'r') as file:
        links = file.read().split('\n')
        print("Done getting links from links.csv")

    header = "first_name, last_name, birth_date, birth_country, ethnicity\n"
    saveData(header)

    for window in range(0, len(links), 100):
        print(f"🎬 Fetching data for window [{window} to {window+100}] celebrities...")
        tempLinks = links[window:window+100]
        tempData = await fetchData(tempLinks)
        saveData(tempData)


async def fetchData(links):
    tempData = ""
    tasks = [getData(link, isSave=False) for link in links]
    with tqdm(total=len(links), desc="Fetching celebrities data...") as pbar:
        for task in asyncio.as_completed(tasks):
            result = await task
            if isinstance(result, str):
                tempData += result
            else:
                print("❗️ Error getting data for ", result["link"])
                continue

            # print(f'Received {data}')
            pbar.desc = f'Received --> {result}'
            pbar.update(1)
    print("✅ Done getting data.")
    return tempData


def saveData(data):
    # saving data to csv file
    with open(saveFile, 'a') as file:
        file.write(data)
        file.close()
    print(f"💾 Data Saved to {saveFile}.")

# run the main function
if __name__ == '__main__':
    asyncio.run(main())
