import pickle
from gensim.models import Word2Vec
from cleantext import removeNoise, lemmatize_verbs
import json

tfidfWeights = pickle.load(open("tfidfWeights.pkl", "rb"))
mlmodel = pickle.load(open("pairsToEmotionsModel.pkl", 'rb'))
word2Vec = Word2Vec.load('twitch_corpus.wv')
emotesToIds = pickle.load(open("emotesToIds.pkl", 'rb'))
emoteToBestEmotion = pickle.load(open("emoteToBestEmotionFixed.pkl","rb"))

bannedEmotes = {"here", "kill", "drop", "drops", "yeah", "does"}

# data = json.load(open('emotes.json'))
# print(data)

# print(emotesToIds)
# print(tfidfWeights['kill'])

def analyzeMessage(message):
    message = message.lower().split()
    result = getMostCommonEmote(message)

    # No emotes in message
    if result is None:
        print("- No emote")
        return None

    emote, message = result
    word = getMostImportantWord(message)
    
    # No recognizable words in message
    if word is None:
        print("- No word")
        if emote in emoteToBestEmotion:
            print("- Emote:", emote, "| Emotion:", emoteToBestEmotion[emote][None])
            return emoteToBestEmotion[emote][None]
        return None

    emotion = mlmodel.predict([word2Vec[emote] + word2Vec[word]])[0]
    print("- Emote:", emote, "| Word:", word, "| Emotion:", emotion)
    return emotion

def getMostCommonEmote(message):
    emoteFreq = {}
    wordFreq = {}

    for word in message:
        if word in emotesToIds and word in word2Vec and word in tfidfWeights and word not in bannedEmotes:
            emoteFreq[word] = emoteFreq.get(word, 0) + 1
        wordFreq[word] = wordFreq.get(word, 0) + 1
    
    if not emoteFreq:
        maxWord = max(wordFreq, key=wordFreq.get)
        if maxWord in emoteToBestEmotion:
            return maxWord, list(filter(lambda a: a != maxWord, message))
        return None
    
    for emote in emoteFreq:
       message = list(filter(lambda a: a != emote, message))

    maxFreq = max(emoteFreq, key=emoteFreq.get)
    mostCommonEmotes = [emote for emote in emoteFreq if emoteFreq[emote] == emoteFreq[maxFreq]]

    importance = {}
    for emote in mostCommonEmotes:
        if emote in tfidfWeights:
            importance[emote] = tfidfWeights[emote]

    if not importance:
        return maxFreq, message

    return min(importance, key=importance.get), message

def getMostImportantWord(message):
    message = removeNoise(' '.join(message))
    importance = {}

    for word in message:
        if word in word2Vec and word in tfidfWeights:
            importance[word] = tfidfWeights[word]

    if not importance:
        return None
    
    return max(importance, key=importance.get)

# testmsg = "LUL LUL Kappa Kappa Kappa LUL that was cmonBruh great sucks awesome lmao"
# testmsg2 = "that was great"
# testmsg3 = "Why do so many of them have alpha boost?"
# testmsg4 = "Pog"
# analyzeMessage(testmsg4)
# print(emoteToBestEmotion["biblethump"])