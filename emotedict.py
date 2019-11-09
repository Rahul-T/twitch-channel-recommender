import json
import pickle

def buildEmoteDicts():
    emotesToIds = {}
    idsToEmotes = {}
    with open('emotes.json') as f:
        data = json.load(f)
        dataList = data['emoticons']
        for index in range(len(dataList)):
            emotesToIds[dataList[index]['code'].lower()] = dataList[index]['id']
            idsToEmotes[dataList[index]['id']] = dataList[index]['code'].lower()
    pickle.dump(emotesToIds, open("emotesToIds.pkl", 'wb+'))
    pickle.dump(idsToEmotes, open("idsToEmotes.pkl", 'wb+'))

buildEmoteDicts()