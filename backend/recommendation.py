import socket
import logging
import os
import re
import requests
from twitch import TwitchHelix
from itertools import islice
from realtimeanalysis import analyzeMessage

server = 'irc.chat.twitch.tv'
port = 6667
nickname = os.environ['TWITCH_USERNAME']
token = os.environ['OAUTH']
client = TwitchHelix(client_id=os.environ['CLIENT_ID'])

def mapGamesToIds():
    gamesToIds = {}
    games_iterator = client.get_top_games(page_size=3)
    for game in islice(games_iterator, 0, 5):
        gamesToIds[game['name']] = game['id']
    print(gamesToIds)
    return gamesToIds

def filterStreams(gameId):
    channels = []
    streams_iterator = client.get_streams()
    streamCount = 0

    for stream in islice(streams_iterator, 0, None):
        if stream['language'] != 'en' or (gameId is not None and gameId != stream['game_id']):
            continue
        channels.append('#' + stream['user_name'].lower())
        streamCount += 1
        if(streamCount == 5):
            break

    print(channels)
    return channels

def getChannelEmotions(channel):
    sock = socket.socket()
    sock.connect((server, port))
    sock.send("PASS {}\n".format(token).encode('utf-8'))
    sock.send("NICK {}\n".format(nickname).encode('utf-8'))
    sock.send("JOIN {}\n".format(channel).encode('utf-8'))

    currentEmotions = {'Anger': 0, 'Disgust': 0, 'Fear': 0, 'Joy': 0, 'Sadness': 0, 'Surprise': 0}
    for x in range(100):
        resp = sock.recv(2048).decode('utf-8')
        message = re.search(':(.*)', resp[1:])
        if not message is None:
            msg = message.group(0)[1:-1]
            print("Message: ", msg)
            emotion = analyzeMessage(msg)
            if emotion is not None:
                currentEmotions[emotion] += 1
    print(currentEmotions)
    return currentEmotions

def analyzeStreams(game, gamesToIds):
    if game is not None:
        game = gamesToIds[game]

    channels = filterStreams(game)

    channelEmotions = {}
    # channels = ['#summit1g', '#nickmercs']
    for channel in channels:
        channelEmotions[channel] = getChannelEmotions(channel)
    print(channelEmotions)
    return channelEmotions

def getRecommendation(emotion, game):
    gamesToIds = mapGamesToIds()
    channelEmotions = analyzeStreams(game, gamesToIds)
    bestStream = max(channelEmotions, key=lambda channel: channelEmotions[channel][emotion])
    print(bestStream[1:])
    return bestStream[1:]

# analyzeStreams()
# getLiveData()
# filterStreams()
# mapGamesToIds()
# getRecommendation()
