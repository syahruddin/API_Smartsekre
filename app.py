import flask
import requests
import json
from flask import request, jsonify ,request ,Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import os
import psycopg2


app = Flask(__name__)
DATABASE_URL = os.environ['postgres://ptcxlcrmcmwcxg:3e55949d90c8570bf69fe7b4c535f18db0f8f42d718f552cacbefdf7ce5c41ab@ec2-54-195-247-108.eu-west-1.compute.amazonaws.com:5432/dco2ka76osf03p']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
#home, kosong
@app.route('/', methods=['GET'])
def home():
    return "<h1>Smart Sekre API</h1> <p>home<p>"

#API SMART SEKRE
@app.route('/getanggota', methods=['GET'])
def getanggota():
    cur.execute("SELECT * FROM keanggotaan;")
    return cur.fetchone()

@app.route('/getstatus', methods=['GET'])
def getstatus():
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/getlog', methods=['GET'])
def getlog():
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/postunit', methods=['POST'])
def postunit():
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/postanggota', methods=['POST'])
def postanggota():
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/postbuka', methods=['POST'])
def postbuka():
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/posttutup', methods=['POST'])
def posttutup():
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/deleteanggota', methods=['DELETE'])
def deleteanggota():
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/deleteunit', methods=['DELETE'])
def deleteunit():
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/updatestatus', methods=['UPDATE'])
def updatestatus():
    return "<h1>Smart Sekre API</h1> <p>home<p>"


#contoh dari api sebelumnya
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
