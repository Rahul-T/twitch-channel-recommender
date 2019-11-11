from flask import Flask, jsonify, request
from recommendation import mapGamesToIds, getRecommendation
import json

app = Flask(__name__)

topGames = None

@app.route('/games', methods=['GET'])
def games():
    global topGames
    topGames = mapGamesToIds()
    resp = json.dumps(list(topGames.keys()))
    return resp

@app.route('/recommendation', methods=['GET'])
def recommendation():
    emotion = request.args.get('emotion')
    game = request.args.get('game')
    print(emotion)
    print(game)
    if game == "Any Game!":
        game = None
    resp = jsonify(getRecommendation(emotion, topGames, game))
    return resp

if __name__ == '__main__':
    app.run(debug=True)