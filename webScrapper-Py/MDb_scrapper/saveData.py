import getData

def saveData(data, fileName='actorsData.csv'):
    with open('./data/' + fileName, 'a') as file:
        file.write(data)
        
# data = getData.getActorData('nm0647634', 'f')
# saveData(data)
