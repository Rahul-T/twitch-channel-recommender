from cleantext import *
import pandas as pd
from emotedict import *

emoteToWordCount = {}

def readData():
    unpickled = pd.read_pickle('ICWSM19_data/ninja.pkl')
    frags = unpickled['fragments']
    limit = 0

    for items in frags.iteritems():
        data = pd.DataFrame(items[1])
        if limit == 10000:
            break
        if('emoticon_id' in data and 'text' in data):
            validText = data[(data['text'] != ' ') & data['text'].notnull()]
            validEmote = data[data.emoticon_id.notnull()]
            if not (validText.empty or validEmote.empty):
                # print(limit)
                limit += 1
                # print("\n")
                emotesInMessage = set()
                for row in validEmote.head().itertuples():
                    emoteId = int(row[1])
                    if(emoteId not in emotesInMessage and emoteId in idsToEmotes):
                        emote = idsToEmotes[emoteId]
                        # print(emote)
                        emotesInMessage.add(emoteId)
                        if emote not in emoteToWordCount:
                            emoteToWordCount[emote] = {}
                        for row in validText.head().itertuples():
                            words = removeNoise(row[2])
                            # print(words)
                            for word in words:
                                if word not in emoteToWordCount[emote]:
                                    emoteToWordCount[emote][word] = 1
                                else:
                                    emoteToWordCount[emote][word] = emoteToWordCount[emote][word] + 1
                                # emoteToWordCount[emote][word] = (emoteToWordCount[emote]).get(word, 0) + 1 
                                # print("emote: ", idsToEmotes[emote], " word: ", word, " count: ", emoteToWordCount[emote][word])
                                # print(row[2])
    for key in emoteToWordCount:
        # print(key)
        srtd = sorted(emoteToWordCount[key], key=emoteToWordCount[key].get, reverse=True)
        emoteToWordCount[key] = srtd[:10]
    print(emoteToWordCount)

                        # print(row[2])
                            # print(row[1])
                            # print(idsToEmotes.get(int(row[1])))