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
    # print(new_words)
    return new_words