import flask
import requests
import json
from flask import request, jsonify ,request ,Flask

app = Flask(__name__)


#masukin api key disini, ingatkan untuk ganti tiap 24 jam
keyAlat = "haiakualatsmartsekre"
keyWeb = "haiakuwebsmartsekre"


#home, kosong
@app.route('/', methods=['GET'])
def home():
    return "<h1>Yasapi</h1> <p>home<p>"

#untuk data2 umum di match tersebut
@app.route('/match/matches_info', methods=['GET'])
def matchinfo():
    if 'match_id' in request.args:
        match_id = int(request.args['match_id'])
    else:
        return "Error: No match field provided. Please specify an match."

    # Create an empty list for our results
    matchdata = {
      "gameDuration": 0,
      "gameId": 0,
      "gameMode": " ",
      "gameType": " ",
      "gameVersion": " ",
      "mapId": 0,
      "teamWin": 0,
      "bans": []
    }

    url = "https://na1.api.riotgames.com/lol/match/v4/matches/" + str(match_id) + "?api_key=" + "apikey"

    response = requests.get(url)

    matchdata['gameDuration'] = response.json()['gameDuration']
    matchdata['gameId'] = response.json()['gameId']
    matchdata['gameMode'] = response.json()['gameMode']
    matchdata['gameType'] = response.json()['gameType']
    matchdata['gameVersion'] = response.json()['gameVersion']
    matchdata['mapId'] = response.json()['mapId']
    matchdata['bans'].extend(response.json()['teams'][0]['bans'])
    matchdata['bans'].extend(response.json()['teams'][1]['bans'])
    if response.json()['teams'][0]['win'] == 'Win':
        matchdata['teamWin'] = 1
    else:
        if response.json()['teams'][1]['win'] == 'Win':
            matchdata['teamWin'] = 2



    return matchdata

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
