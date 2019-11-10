import pickle
import numpy
import scipy
from sklearn import svm
from gensim.models import Word2Vec
import gensim 
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

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
        emoteVec = model['monkas']
        wordVec = model['chat']
        res = mlmodel.predict([emoteVec + wordVec])
        print(res)

def tfidf():
    vectorizer = TfidfVectorizer(strip_accents='ascii', stop_words='english')
    with open("chat_logs_processed.txt", 'r') as f:
        content = f.readlines()
        vectorizer.fit_transform(content)
    pickle.dump(vectorizer, open("vectorizer.pkl", 'wb+'))
    print(vectorizer.get_feature_names())

# startTime = datetime.datetime.now()
# tfidf()
def createWeightsDict():
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
    idf = vectorizer.idf_
    weights = dict(zip(vectorizer.get_feature_names(), idf))
    pickle.dump(weights, open("tfidfWeights.pkl", "wb+"))

# weights = pickle.load(open("tfidfWeights.pkl", "rb"))
# testmsg = "LUL that was great"
# for word in testmsg.split():
#     try:
#         print(word, " ", weights[word])
#     except:
#         continue


# print(sorted(weights.items(), key=lambda x: x[1]))

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