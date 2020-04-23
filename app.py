import flask
import requests
import json
from flask import request, jsonify ,request ,Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import os
import psycopg2


app = Flask(__name__)
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
#home, kosong
@app.route('/', methods=['GET'])
def home():
    return "<h1>Smart Sekre API</h1> <p>home<p>"

#API SMART SEKRE
@app.route('/getanggota', methods=['GET'])
def getanggota():
    if 'id_unit' in request.args:
        id_unit = int(request.args['id_unit'])
    else:
        return "Error"
    cur.execute("SELECT * FROM keanggotaan WHERE id_unit = %s;",[id_unit])
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/getstatus', methods=['GET'])
def getstatus():
    cur.execute("SELECT * FROM unit;")
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/getlog', methods=['GET'])
def getlog():
    cur.execute("SELECT * FROM log_sekre;")
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/postunit', methods=['POST','GET'])
def postunit():
    if 'id_unit' in request.args:
        id_unit = int(request.args['id_unit'])
    else:
        return "Error"
    if 'nama' in request.args:
        nama = request.args['nama']
    else:
        return "Error"

    cur.execute("INSERT INTO unit(id_unit,nama,status_pintu,status_listrik) VALUES (%s,%s,false,false);",(id_unit,nama))
    conn.commit()
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/postanggota', methods=['POST','GET'])
def postanggota():
    if 'id_unit' in request.args:
        id_unit = int(request.args['id_unit'])
    else:
        return "Error"
    if 'nama' in request.args:
        nama = request.args['nama']
    else:
        return "Error"
    if 'id_mahasiswa' in request.args:
        id_mahasiswa = int(request.args['id_mahasiswa'])
    else:
        return "Error"
    cur.execute("INSERT INTO keanggotaan(id_unit,nama,id_mahasiswa) VALUES (%s,%s,%s);",(id_unit,nama,id_mahasiswa))
    conn.commit()
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/postbuka', methods=['POST','GET'])
def postbuka():
    if 'id_unit' in request.args:
        id_unit = int(request.args['id_unit'])
    else:
        return "Error"
    if 'id_mahasiswa' in request.args:
        id_mahasiswa = int(request.args['id_mahasiswa'])
    else:
        return "Error"
    cur.execute("INSERT INTO log_sekre(id_unit,nama,id_mahasiswa,transaksi,waktu) VALUES (%s,%s,true,GETDATE());",(id_unit,id_mahasiswa))
    conn.commit()
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/posttutup', methods=['POST','GET'])
def posttutup():
    if 'id_unit' in request.args:
        id_unit = int(request.args['id_unit'])
    else:
        return "Error"
    if 'id_mahasiswa' in request.args:
        id_mahasiswa = int(request.args['id_mahasiswa'])
    else:
        return "Error"
    cur.execute("INSERT INTO log_sekre(id_unit,nama,id_mahasiswa,transaksi,waktu) VALUES (%s,%s,false,GETDATE());",(id_unit,id_mahasiswa))
    conn.commit()
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/deleteanggota', methods=['DELETE','GET'])
def deleteanggota():
    if 'id_unit' in request.args:
        id_unit = int(request.args['id_unit'])
    else:
        return "Error"
    if 'id_mahasiswa' in request.args:
        id_mahasiswa = int(request.args['id_mahasiswa'])
    else:
        return "Error"
    cur.execute("DELETE FROM keanggotaan WHERE id_unit = %s AND id_mahasiswa = %s;",(id_unit,id_mahasiswa))
    conn.commit()
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/deleteunit', methods=['DELETE','GET'])
def deleteunit():
    if 'id_unit' in request.args:
        id_unit = int(request.args['id_unit'])
    else:
        return "Error"
    cur.execute("DELETE FROM keanggotaan WHERE id_unit = %s;",(id_unit))
    cur.execute("DELETE FROM unit WHERE id_unit = %s;",(id_unit))
    conn.commit()
    return "<h1>Smart Sekre API</h1> <p>home<p>"

@app.route('/updatestatus', methods=['UPDATE','GET'])
def updatestatus():
    if 'id_unit' in request.args:
        id_unit = int(request.args['id_unit'])
    else:
        return "Error"
    if 'status_pintu' in request.args:
        if int(request.args['status_pintu']) == 1:
            pintu = True
        else:
            pintu = False
    else:
        return "Error"
        if 'status_listrik' in request.args:
            if int(request.args['status_listrik']) == 1:
                listrik = True
            else:
                listrik = False
        else:
            return "Error"
    cur.execute("UPDATE unit SET status_pintu = %s,status_listrik= %s WHERE id_unit = %s;",(pintu,listrik,id_unit))
    conn.commit()
    return "<h1>Smart Sekre API</h1> <p>home<p>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
