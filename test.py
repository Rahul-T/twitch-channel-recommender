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

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

unpickled = pd.read_pickle('ICWSM19_data/ninja.pkl')
frags = unpickled['fragments']

for items in frags.iteritems():
    # print(items[1])
    data = pd.DataFrame(items[1])
    # print(items[1])
    # data = [json.loads(i) for i in data if i]    #Iterate your list check if you have data then use json.loads
    # print("\nnewframe")
    if('emoticon_id' in data and 'text' in data):
        # print(data[data.emoticon_id.notnull()])
        data2 = data[data['text'] != ' ']
        data3 = data2[data['text'].notnull()]
        if not data3.empty:
            print(items[1])
            print(data3)


# print(type(frags))
# js = [json.loads(i) for i in frags if i]



# for x in range(100):
#     resp = sock.recv(2048).decode('utf-8')
#     print(resp)