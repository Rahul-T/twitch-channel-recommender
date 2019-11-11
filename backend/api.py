from flask import Flask, jsonify, request
from recommendation import mapGamesToIds, getRecommendation

app = Flask(__name__)

topGames = None

@app.route('/games', methods=['GET'])
def games():
    global topGames
    topGames = mapGamesToIds()
    resp = jsonify(list(topGames.keys()))
    return resp

@app.route('/recommendation', methods=['GET'])
def recommendation():
    emotion = request.args.get('emotion')
    game = request.args.get('game')
    resp = jsonify(getRecommendation(emotion, topGames, game))
    return resp

if __name__ == '__main__':
    app.run(debug=True)