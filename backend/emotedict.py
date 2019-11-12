import json
import pickle

def buildEmoteDicts():
    emotesToIds = {}
    idsToEmotes = {}
    with open('models/emotes.json') as f:
        data = json.load(f)
        dataList = data['emoticons']
        for index in range(len(dataList)):
            emotesToIds[dataList[index]['code'].lower()] = dataList[index]['id']
            idsToEmotes[dataList[index]['id']] = dataList[index]['code'].lower()
    pickle.dump(emotesToIds, open("models/emotesToIds.pkl", 'wb+'))
    pickle.dump(idsToEmotes, open("models/idsToEmotes.pkl", 'wb+'))

buildEmoteDicts()