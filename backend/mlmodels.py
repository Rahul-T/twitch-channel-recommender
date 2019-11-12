import pickle
import numpy
import scipy
from sklearn import svm
from gensim.models import Word2Vec
import gensim 
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

# Formats dataset from static map to train ml model
def formatDataset():
    with open("models/emoteToBestEmotion.pkl","rb") as f:
        emoteToBestEmotion = pickle.load(f)

    # Code for training word2vec found here
    # https://github.com/evanslt/BlogCode/tree/master/NLP
    model = Word2Vec.load('models/twitch_corpus.wv')
    data = []
    targets = []

    for emote in emoteToBestEmotion.keys():
        for word in emoteToBestEmotion[emote]:
            try:
                emoteVec = model[emote.lower()]
                wordVec = model[word.lower()]
            except:
                continue
            pair = emoteVec + wordVec
            emotion = emoteToBestEmotion[emote][word]
            data.append(pair)
            targets.append(emotion)

    return data, targets

def trainModel():
    data, targets = formatDataset()
    clf = svm.SVC(gamma=0.001, C=100)
    x,y = data, targets
    clf.fit(x,y)
    pickle.dump(clf, open("models/pairsToEmotionsModel.pkl", 'wb+'))

# tfidf gets frequencies of words and is used because the less frequent a word
# is, the more important it is to the meaning of the sentence
def tfidf():
    vectorizer = TfidfVectorizer(strip_accents='ascii', stop_words='english')
    with open("models/chat_logs_processed.txt", 'r') as f:
        content = f.readlines()
        vectorizer.fit_transform(content)
    pickle.dump(vectorizer, open("models/vectorizer.pkl", 'wb+'))

def createWeightsDict():
    vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))
    idf = vectorizer.idf_
    weights = dict(zip(vectorizer.get_feature_names(), idf))
    pickle.dump(weights, open("models/tfidfWeights.pkl", "wb+"))