import pickle
from gensim.models import Word2Vec
from cleantext import removeNoise, lemmatize_verbs
import json

tfidfWeights = pickle.load(open("models/tfidfWeights.pkl", "rb"))
mlmodel = pickle.load(open("models/pairsToEmotionsModel.pkl", 'rb'))
word2Vec = Word2Vec.load('models/twitch_corpus.wv')
emotesToIds = pickle.load(open("models/emotesToIds.pkl", 'rb'))
emoteToBestEmotion = pickle.load(open("models/emoteToBestEmotionFixed.pkl","rb"))

# Some emotes like "herE" are synonymous with common words so they must be dropped
bannedEmotes = {"here", "kill", "drop", "drops", "yeah", "does"}

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
        # Checks static map of emotes as backup for emote-only message
        # e.g. [LUL, None] mapping
        if emote in emoteToBestEmotion:
            print("- Emote:", emote, "| Emotion:", emoteToBestEmotion[emote][None])
            return emoteToBestEmotion[emote][None]
        return None

    # Gets emotion from ML model
    emotion = mlmodel.predict([word2Vec[emote] + word2Vec[word]])[0]
    print("- Emote:", emote, "| Word:", word, "| Emotion:", emotion)
    return emotion

def getMostCommonEmote(message):
    emoteFreq = {}
    wordFreq = {}

    # Gets emote frequencies
    for word in message:
        if word in emotesToIds and word in word2Vec and word in tfidfWeights and word not in bannedEmotes:
            emoteFreq[word] = emoteFreq.get(word, 0) + 1
        wordFreq[word] = wordFreq.get(word, 0) + 1
    
    # If no emotes found, searches static map as a last chance
    if not emoteFreq:
        maxWord = max(wordFreq, key=wordFreq.get)
        if maxWord in emoteToBestEmotion:
            return maxWord, list(filter(lambda a: a != maxWord, message))
        return None
    
    # Removes emotes from message
    for emote in emoteFreq:
       message = list(filter(lambda a: a != emote, message))

    # Gets all emotes with highest frequency
    maxFreq = max(emoteFreq, key=emoteFreq.get)
    mostCommonEmotes = [emote for emote in emoteFreq if emoteFreq[emote] == emoteFreq[maxFreq]]

    # Gets emote of least importance (most frequent) according to tfidf
    # if there are multiple emotes with highest frequency
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

    # Most important word is the least common via tfidf
    for word in message:
        if word in word2Vec and word in tfidfWeights:
            importance[word] = tfidfWeights[word]

    if not importance:
        return None
    
    return max(importance, key=importance.get)