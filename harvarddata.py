from cleantext import *
import pandas as pd
from emotedict import *
import datetime
import twitter_emotion_recognition.emotion_predictor as twitter
from collections import Counter 
import os
import pickle

# We only want messages that contain both emotes and text
def checkEmoteAndText(data):
    if('emoticon_id' in data and 'text' in data):
        validText = data[(data['text'] != ' ') & data['text'].notnull()]
        validEmote = data[data.emoticon_id.notnull()]
        if not (validText.empty or validEmote.empty):
            return validText, validEmote
    return None, None

def clusterFile(frags, model, emoteToWordCount, emoteToEmotionCount):
    limit = 0

    for items in frags.iteritems():
        if limit == 100:
            break
        limit += 1

        # Items looks like: (30397, [{'emoticon_id': '822112'}, {'text': ' '}])
        # First element is an id which we don't need
        data = pd.DataFrame(items[1])
        validText, validEmote = checkEmoteAndText(data)
        if(validText is None and validEmote is None):
            continue

        emotesInMessage = set()
        for row in validEmote.head().itertuples():
            emoteId = int(row[1])
            if(emoteId not in emotesInMessage and emoteId in idsToEmotes):
                emote = idsToEmotes[emoteId]
                emotesInMessage.add(emoteId)
                if emote not in emoteToWordCount:
                    emoteToWordCount[emote] = {}
                    emoteToEmotionCount[emote] = {}
                for row in validText.head().itertuples():
                    words = removeNoise(row[2])
                    strList = []
                    strList.append(row[2])
                    predictions = model.predict_classes(strList)
                    mood = predictions.values[0][1]
                    for word in words:
                        if word not in emoteToWordCount[emote]:
                            emoteToWordCount[emote][word] = 1
                            emoteToEmotionCount[emote][word] = {'Anger': 0, 'Disgust': 0, 'Fear': 0, 'Joy': 0, 'Sadness': 0, 'Surprise': 0}
                            emoteToEmotionCount[emote][word][mood] = 1
                        else:
                            emoteToWordCount[emote][word] = emoteToWordCount[emote][word] + 1
                            emoteToEmotionCount[emote][word][mood] = emoteToEmotionCount[emote][word][mood] + 1

    for emote in emoteToWordCount:
        srtd = sorted(emoteToWordCount[emote], key=emoteToWordCount[emote].get, reverse=True)
        emoteToWordCount[emote] = srtd[:10]

    for emote in emoteToEmotionCount.copy():
        for word in emoteToEmotionCount[emote].copy():
            if word not in emoteToWordCount[emote]:
                del emoteToEmotionCount[emote][word]

    emoteToBestEmotion = {}
    for emote in emoteToEmotionCount:
        emoteToBestEmotion[emote] = {}
        for word in emoteToEmotionCount[emote]:
            emoteToBestEmotion[emote][word] = max(emoteToEmotionCount[emote][word], key=emoteToEmotionCount[emote][word].get)
        if(emoteToBestEmotion[emote]):
            value, count = Counter(emoteToBestEmotion[emote].values()).most_common(1)[0]
            emoteToBestEmotion[emote][None] = value

    # f = open("emotemapping.pkl","wb")
    # pickle.dump(emoteToBestEmotion, f)
    # f = open("emotemapping.pkl","rb")
    # dd = pickle.load(f)
    # print(dd)
    print("\nBREAK\n")
    print(emoteToBestEmotion)
    return emoteToWordCount, emoteToBestEmotion

def emoteCluster():
    emoteToWordCount = {}
    emoteToEmotionCount = {}
    model = twitter.EmotionPredictor(classification='ekman', setting='mc', use_unison_model=True)
    # for filename in os.listdir('ICWSM19_data'):
    #     print(filename)
    startTime = datetime.datetime.now()
    filename = 'ninja.pkl'
    path = 'ICWSM19_data/' + filename
    unpickled = pd.read_pickle(path)
    frags = unpickled['fragments']
    
    emoteToWordCount, emoteToEmotionCount = clusterFile(frags, model, emoteToWordCount, emoteToEmotionCount)
    print(emoteToWordCount)
    print("\nBREAK\n")
    print(emoteToEmotionCount)
    print("Start: ", startTime)
    print("End: ", datetime.datetime.now())