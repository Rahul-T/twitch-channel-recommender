import pickle


# Converts emote dict to lowercase
with open("models/emoteToBestEmotion.pkl","rb") as f:
    emoteToBestEmotion = pickle.load(f)
    emotelowers = {}

    for emote in emoteToBestEmotion:
        emotelowercase = emote.lower()
        emotelowers[emotelowercase] = {}
        for word in emoteToBestEmotion[emote]:
            emotelowers[emotelowercase][word] = emoteToBestEmotion[emote][word]

    # Manual overrides to improve accuracy and include some BTTV emotes
    emotelowers['notlikethis'][None] = 'Sadness'
    emotelowers['lul'][None] = 'Joy'
    emotelowers['cmonbruh'][None] = 'Anger'
    emotelowers['monkas'][None] = 'Fear'
    emotelowers['biblethump'][None] = 'Sadness'
    emotelowers['pog'] = {}
    emotelowers['pog'][None] = 'Joy'
    emotelowers['kekw'] = {}
    emotelowers['kekw'][None] = 'Joy'
    emotelowers['lulw'] = {}
    emotelowers['lulw'][None] = 'Joy'
    emotelowers['omegalul'] = {}
    emotelowers['omegalul'][None] = 'Joy'
    emotelowers['pepehands'] = {}
    emotelowers['pepehands'][None] = 'Sadness'

    with open("models/emoteToBestEmotionFixed.pkl","wb+") as f:
        pickle.dump(emotelowers, f)