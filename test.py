import socket
import logging
import os
import pandas as pd

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
print(unpickled['body'])

# for x in range(100):
#     resp = sock.recv(2048).decode('utf-8')
#     print(resp)