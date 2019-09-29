import socket
import logging
import os
import pandas as pd
import json

server = 'irc.chat.twitch.tv'
port = 6667
nickname = os.environ['TWITCH_USERNAME']
token = os.environ['OAUTH']
channel = '#shroud'

sock = socket.socket()
sock.connect((server, port))

sock.send("PASS {}\n".format(token).encode('utf-8'))
sock.send("NICK {}\n".format(nickname).encode('utf-8'))
sock.send("JOIN {}\n".format(channel).encode('utf-8'))

unpickled = pd.read_pickle('ICWSM19_data/ninja.pkl')
frags = unpickled['fragments']

for items in frags.iteritems():
    data = pd.DataFrame(items[1])

    if('emoticon_id' in data and 'text' in data):
        validText = data[(data['text'] != ' ') & data['text'].notnull()]
        validEmote = data[data.emoticon_id.notnull()]
        if not (validText.empty or validEmote.empty):
            print(items[1])

# for x in range(100):
#     resp = sock.recv(2048).decode('utf-8')
#     print(resp)