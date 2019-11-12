from cleantext import *
import pandas as pd
from emotedict import *
import datetime
import twitter_emotion_recognition.emotion_predictor as twitter
from collections import Counter 
import os
import pickle

# We only want messages with both emotes and text
def checkEmoteAndText(data):
    if('emoticon_id' in data and 'text' in data):
        validText = data[(data['text'] != ' ') & data['text'].notnull()]
        validEmote = data[data.emoticon_id.notnull()]
        if not (validText.empty or validEmote.empty):
            return validText, validEmote
    return None, None

# Builds nested dict mapping emote-word pairs to mood
def mapEmoteWordsToMood(emote, emoteToWordCount, emoteToEmotionCount, cleanWords, mood):
    # Add emote to overarching dicts if first occurence
    if emote not in emoteToWordCount:
        emoteToWordCount[emote] = {}
        emoteToEmotionCount[emote] = {}

    for word in cleanWords:
        if word not in emoteToWordCount[emote]:
            emoteToWordCount[emote][word] = 1
            emoteToEmotionCount[emote][word] = {'Anger': 0, 'Disgust': 0, 'Fear': 0, 'Joy': 0, 'Sadness': 0, 'Surprise': 0}
            emoteToEmotionCount[emote][word][mood] = 1
        else:
            emoteToWordCount[emote][word] = emoteToWordCount[emote][word] + 1
            emoteToEmotionCount[emote][word][mood] = emoteToEmotionCount[emote][word][mood] + 1

# Uses sentiment analyzer to get mood of all words in context
# https://github.com/nikicc/twitter-emotion-recognition
def analyzeText(validText, model):
    rawWords = []
    cleanWords = []
    for row in validText.head().itertuples():
        cleanWords.extend(removeNoise(row[2]))
        rawWords.append(row[2])

    predictions = model.predict_classes([' '.join(rawWords)])
    mood = predictions.values[0][1]
    return cleanWords, mood

# Gets 10 most common words associated with emote to build final mapping
def getTopWords(emoteToWordCount, emoteToEmotionCount):
    for emote in emoteToWordCount:
        srtd = sorted(emoteToWordCount[emote], key=emoteToWordCount[emote].get, reverse=True)
        emoteToWordCount[emote] = srtd[:10]

    for emote in emoteToEmotionCount.copy():
        for word in emoteToEmotionCount[emote].copy():
            if word not in emoteToWordCount[emote]:
                del emoteToEmotionCount[emote][word]

# Maps emote-word pair to most common emotion and sets default 'None' value to
# most common emotion associated with emote
def mapEmoteToBestEmotions(emoteToEmotionCount):
    emoteToBestEmotion = {}
    for emote in emoteToEmotionCount:
        emoteToBestEmotion[emote] = {}
        for word in emoteToEmotionCount[emote]:
            emoteToBestEmotion[emote][word] = max(emoteToEmotionCount[emote][word], key=emoteToEmotionCount[emote][word].get)
        if(emoteToBestEmotion[emote]):
            value, count = Counter(emoteToBestEmotion[emote].values()).most_common(1)[0]
            emoteToBestEmotion[emote][None] = value
    return emoteToBestEmotion

# Iterates over lines of individual file to build out emote mappings
def clusterFile(frags, emoteToWordCount, emoteToEmotionCount, model):
    for items in frags.iteritems():
        # Items looks like: (30397, [{'emoticon_id': '822112'}, {'text': ' '}])
        # First element is an id which we don't need
        data = pd.DataFrame(items[1])
        validText, validEmote = checkEmoteAndText(data)

        # We can only use messages with both emotes and text
        if(validText is None and validEmote is None):
            continue
        
        emotesInMessage = set()
        cleanWords, mood = analyzeText(validText, model)

        # Iterate over emotes and map word/mood accordingly
        for row in validEmote.head().itertuples():
            emoteId = int(row[1])
            # Skip if repeat emote or emoteId not found in database
            if emoteId in emotesInMessage or emoteId not in idsToEmotes:
                continue
            emotesInMessage.add(emoteId)
            mapEmoteWordsToMood(idsToEmotes[emoteId], emoteToWordCount, emoteToEmotionCount, cleanWords, mood)

    return emoteToWordCount, emoteToEmotionCount

# Iterates over all files in dataset found at
# https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VE0IVQ
def emoteCluster():
    with open("models/emoteToWordCount.pkl","rb+") as f3:
        emoteToWordCount = pickle.load(f3)
    with open("models/emoteToEmotionCount.pkl","rb+") as f4:
        emoteToEmotionCount = pickle.load(f4)

    model = twitter.EmotionPredictor(classification='ekman', setting='mc', use_unison_model=True)
    
    startTime = datetime.datetime.now()
    for filename in os.listdir('ICWSM19_data'):
        if filename == '.DS_Store':
            continue
        print(filename)
        path = 'ICWSM19_data/' + filename
        unpickled = pd.read_pickle(path)
        frags = unpickled['fragments']

        emoteToWordCount, emoteToEmotionCount = clusterFile(frags, emoteToWordCount, emoteToEmotionCount, model)

        print("Writing out dicts")
        with open("models/emoteToWordCount.pkl","wb") as f1:
            pickle.dump(emoteToWordCount, f1)
        with open("models/emoteToEmotionCount.pkl","wb") as f2:
            pickle.dump(emoteToEmotionCount, f2)
        print("Wrote out dicts")

        print("Reading in dicts")
        with open("models/emoteToWordCount.pkl","rb") as f5:
            emoteToWordCount = pickle.load(f5)
        with open("models/emoteToEmotionCount.pkl","rb") as f6:
            emoteToEmotionCount = pickle.load(f6)
        print("Read in dicts")

    getTopWords(emoteToWordCount, emoteToEmotionCount)
    emoteToBestEmotion = mapEmoteToBestEmotions(emoteToEmotionCount)
    with open("models/emoteToBestEmotion.pkl","wb") as f5:
        pickle.dump(emoteToBestEmotion, f5)

    print(emoteToBestEmotion)

    print("Start: ", startTime)
    print("End: ", datetime.datetime.now())