import flask
import requests
import json
from flask import request, jsonify ,request ,Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)

keyAlat = "haiakualatsmartsekre"
keyWeb = "haiakuwebsmartsekre"

class Dataentry(db.Model):
    __tablename__ = "dataentry"
    id = db.Column(db.Integer, primary_key=True)
    mydata = db.Column(db.Text())

    def __init__ (self, mydata):
        self.mydata = mydata


@app.route("/submit", methods=["POST"])
def post_to_db():
    indata = Dataentry(request.form['mydata'])
    data = copy(indata. __dict__ )
    del data["_sa_instance_state"]
    try:
        db.session.add(indata)
        db.session.commit()
    except Exception as e:
        print("\n FAILED entry: {}\n".format(json.dumps(data)))
        print(e)
        sys.stdout.flush()
    return 'Success! To enter more data, <a href="{}">click here!</a>'.format(url_for("enter_data"))


#home, kosong
@app.route('/', methods=['GET'])
def home():
    return "<h1>Smart Sekre API</h1> <p>home<p>"

#API SMART SEKRE
@app.route('/getanggota', methods=['GET'])
def getanggota():
    result = db.engine.execute(tect('select * from keanggotaan'))
    return result

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
