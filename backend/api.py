from flask import Flask, jsonify, request
from recommendation import mapGamesToIds, getRecommendation

app = Flask(__name__)

@app.route('/games', methods=['GET'])
def games():
    resp = jsonify(mapGamesToIds())
    return resp

@app.route('/recommendation', methods=['GET'])
def recommendation():
    emotion = request.args.get('emotion')
    game = request.args.get('game')
    resp = jsonify(getRecommendation(emotion, game))
    return resp

if __name__ == '__main__':
    app.run(debug=True)