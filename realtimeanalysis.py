import pickle
from gensim.models import Word2Vec

tfidfWeights = pickle.load(open("tfidfWeights.pkl", "rb"))
mlmodel = pickle.load(open("pairsToEmotionsModel.pkl", 'rb'))
word2Vec = Word2Vec.load('twitch_corpus.wv')
emotesToIds = pickle.load(open("emotesToIds.pkl", 'rb'))

def analyzeMessage(message):
    message = message.lower().split()
    result = getMostCommonEmote(message)

    # No emotes in message
    if result is None:
        return None

    emote, message = result
    word = getMostImportantWord(message)
    
    # No recognizable words in message
    if word is None:
        return None

    # print(emote)
    # print(word)
    emotion = mlmodel.predict([word2Vec[emote] + word2Vec[word]])
    print(emotion[0])
    return emotion[0]

def getMostCommonEmote(message):
    emoteFreq = {}

    for word in message:
        if word in emotesToIds and word in word2Vec:
            emoteFreq[word] = emoteFreq.get(word, 0) + 1
    
    if not emoteFreq:
        return None

    for emote in emoteFreq:
       message = list(filter(lambda a: a != emote, message))

    return max(emoteFreq, key=emoteFreq.get), message

def getMostImportantWord(message):
    importance = {}
    for word in message:
        if word in word2Vec and word in tfidfWeights:
            importance[word] = tfidfWeights[word]

    if not importance:
        return None
    
    return max(importance, key=importance.get)

testmsg = "LUL LUL Kappa cmonBruh LUL that was cmonBruh great sucks awesome lmao"
testmsg2 = "that was great"
analyzeMessage(testmsg)