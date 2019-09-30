import socket
import logging
import os
import pandas as pd
import json
import re, string, unicodedata
import nltk
import contractions
import inflect
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

server = 'irc.chat.twitch.tv'
port = 6667
nickname = os.environ['TWITCH_USERNAME']
token = os.environ['OAUTH']
channel = '#twitch'

sock = socket.socket()
sock.connect((server, port))

sock.send("PASS {}\n".format(token).encode('utf-8'))
sock.send("NICK {}\n".format(nickname).encode('utf-8'))
sock.send("JOIN {}\n".format(channel).encode('utf-8'))

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

def removeNoise(text):
    p = inflect.engine()
    text = re.sub('\[[^]]*\]', '', text)
    text = contractions.fix(text)
    words = nltk.word_tokenize(text)
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_word = new_word.lower()
        new_word = re.sub(r'[^\w\s]', '', new_word)
        if new_word != '' and new_word not in stopwords.words('english'):
            if word.isdigit():
                new_word = p.number_to_words(new_word)
            new_words.append(new_word)
    new_words = lemmatize_verbs(new_words)
    print(new_words)
    return new_words

def readData():
    unpickled = pd.read_pickle('ICWSM19_data/ninja.pkl')
    frags = unpickled['fragments']

    for items in frags.iteritems():
        data = pd.DataFrame(items[1])

        if('emoticon_id' in data and 'text' in data):
            validText = data[(data['text'] != ' ') & data['text'].notnull()]
            validEmote = data[data.emoticon_id.notnull()]
            if not (validText.empty or validEmote.empty):
                print("\n")
                for row in validText.head().itertuples():
                    removeNoise(row[2])
                    # print(row[2])
                for row in validEmote.head().itertuples():
                    print(row[1])

def getLiveData():
    for x in range(100):
        resp = sock.recv(2048).decode('utf-8')
        # msg = resp.split(':')
        # print(msg)

def getEmotes():
    emoteDict = {}
    with open('emotes.json') as f:
        data = json.load(f)
        dataList = data['emoticons']
        for index in range(len(dataList)):
            emoteDict[dataList[index]['code']] = dataList[index]['id']
    return emoteDict

# readData()
# getEmotes()
# getLiveData()