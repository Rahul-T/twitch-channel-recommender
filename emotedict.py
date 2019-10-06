import json

def buildEmoteDicts():
    emotesToIds = {}
    idsToEmotes = {}
    with open('emotes.json') as f:
        data = json.load(f)
        dataList = data['emoticons']
        for index in range(len(dataList)):
            emotesToIds[dataList[index]['code']] = dataList[index]['id']
            idsToEmotes[dataList[index]['id']] = dataList[index]['code']
    return (emotesToIds, idsToEmotes)

emotesToIds, idsToEmotes = buildEmoteDicts()