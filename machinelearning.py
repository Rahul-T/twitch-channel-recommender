import pickle
import numpy
import scipy
from sklearn import svm
from gensim.models import Word2Vec
import gensim 
import datetime

def formatDataset():
    with open("emoteToBestEmotion.pkl","rb") as f:
        emoteToBestEmotion = pickle.load(f)
    model = Word2Vec.load('twitch_corpus.wv')

    success = 0
    fails = 0

    data = []
    targets = []
    for emote in emoteToBestEmotion.keys():
        for word in emoteToBestEmotion[emote]:
            try:
                emoteVec = model[emote.lower()]
                wordVec = model[word.lower()]
            except:
                fails += 1
                continue
            success += 1
            pair = emoteVec + wordVec
            emotion = emoteToBestEmotion[emote][word]
            data.append(pair)
            targets.append(emotion)
    # print(data)
    # print(success)
    # print(fails)
    return data, targets


def trainModel():
    data, targets = formatDataset()
    # data = [[[1.0, 2.0], [3.0, 4.0]], [[6.0, 7.0], [8.0, 9.0]]]
    # targets = ['joy', 'fear']
    clf = svm.SVC(gamma=0.001, C=100)
    x,y = data, targets
    clf.fit(x,y)
    pickle.dump(clf, open("pairsToEmotionsModel.pkl", 'wb+'))
    print(clf.predict(data))

def testModel():
    with open("pairsToEmotionsModel.pkl", 'rb') as pickle_file:
        mlmodel = pickle.load(pickle_file)
        model = Word2Vec.load('twitch_corpus.wv')
        emoteVec = model['cmonbruh']
        wordVec = model['fuck']
        res = mlmodel.predict([emoteVec + wordVec])
        print(res)

testModel()

def testCode():
    #trainModel()
    with open("emoteToBestEmotion.pkl","rb") as f:
        emoteToBestEmotion = pickle.load(f)

    model = Word2Vec.load('twitch_corpus.wv')
    # model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

    # tmpEm = 'BibleThump'
    # print(model.most_similar(positive=[tmpEm.lower()]))
    # print(emoteToBestEmotion[tmpEm])
    # print(model.most_similar(positive=['go']))
    # print(model['kekw'])
    emotesfound = 0
    emotesnotfound = 0

    for emote in emoteToBestEmotion.keys():
        try:
            x = model[emote.lower()]
            emotesfound += 1
        except:
            emotesnotfound += 1
            continue

    print("emotesfound: ", emotesfound)
    print("emotesnotfound: ", emotesnotfound)

    wordsfound = 0
    wordsnotfound = 0

    for emote in emoteToBestEmotion.keys():
        for word in emoteToBestEmotion[emote]:
            try:
                x = model[word]
                wordsfound += 1
            except:
                if word is not None:
                    wordsnotfound += 1
                continue

    print("wordsfound: ", wordsfound)
    print("wordsnotfound: ", wordsnotfound)

# testCode()
# formatDataset()