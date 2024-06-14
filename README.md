<img alt="NameGenerator_Logo" style="display: block; margin-left: auto; margin-right: auto;" height="150" width="150" src="NameGenerator_Logo.png">


# Name Generator

- Developed a name generation AI utilizing PyTorch and NumPy to construct a Deep Learning LSTM model, ensuring accurate and culturally relevant name suggestions.
- Integrated BeautifulSoup, AsyncIO, and Request to efficiently web-scrap diverse datasets containing names from various ethnicities and cultures, enhancing the training process.
- Initiated the project with a GAN-based model approach, swiftly pivoting to the LSTM model to achieve desired outcomes and improve name generation accuracy.
- Engineered a user-friendly web interface using Flask Python framework, facilitating seamless interaction and accessibility for users.
- Implemented cloud deployment on an AWS EC2 instance of Ubuntu, leveraging scalability and accessibility benefits for the hosted website.

## Frameworks and Libraries
- PyTorch
- TQDM
- NumPy
- SciKitLearn
- BeautifulSoup
- AsynclO
- Requests

## Demo Video

[![Demo Video](https://img.youtube.com/vi/XETwXTNgrQs/0.jpg)](https://www.youtube.com/watch?v=XETwXTNgrQs)

## Run the web app
> cd website   
> pip install -r requirements.txt   
> python app.py

## Run web scraper
> cd webScrapper-Py/MDb_scraper     
> python3 start.py 
- You will get .csv files in the `webScrapper-Py` folder with name `actorsData.csv`.

## Run tests
> pytest -vv

Know more about the project [here](https://jeel.notion.site/Name-Generator-1887434654f84df5812b3adf8c8544b8?pvs=4)
