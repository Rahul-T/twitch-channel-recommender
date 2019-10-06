import socket
import logging
import os
from cleantext import *
from harvarddata import *
from emotedict import *

server = 'irc.chat.twitch.tv'
port = 6667
nickname = os.environ['TWITCH_USERNAME']
token = os.environ['OAUTH']
channel = '#nickmercs'

sock = socket.socket()
sock.connect((server, port))

sock.send("PASS {}\n".format(token).encode('utf-8'))
sock.send("NICK {}\n".format(nickname).encode('utf-8'))
sock.send("JOIN {}\n".format(channel).encode('utf-8'))

def getLiveData(ed):
    for x in range(100):
        resp = sock.recv(2048).decode('utf-8')
        message = re.search(':(.*)', resp[1:])
        if not message is None:
            msg = message.group(0)[1:-1].split(' ')
            print(msg)
            for word in msg:
                if word in ed:
                    print(ed[word])


readData()
# emotesToIds, idsToEmotes = buildEmoteDicts()
# print(emotesToIds.get('Kappa'))
# print(idsToEmotes.get(1))
# getLiveData(ed)