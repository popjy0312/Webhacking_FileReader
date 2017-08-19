#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import *
import os
import hashlib

app = Flask(__name__)

app.secret_key = '#######################################'  #secret key

def check_is_flag(data):
    data = hashlib.sha256(data).hexdigest()
    
    if data == "c3065ded789a1f36072cd8d03b2c4626e3835419971078108e1f138396432d82":
        return 1
    return 0


@app.route('/')
def main():
    session.clear()
    lists = os.listdir('./files')
    return render_template('main.html', files=lists)

@app.route('/readFile', methods = ['GET'])
def openFile():
    fileName = request.args.get('fileName')

    #filter
    if fileName not in os.listdir('./files'):
        session.clear()
        return "file open fail"

    if session.get('fileFlag') == True:
        session.pop('fileData', None)
    session['fileFlag'] = True
    with open("files/" + fileName ,"r") as f:
        datas = f.readlines()
        data = "\n".join(i for i in datas)
    session['fileData'] = data

    return redirect('/checkFlag')

@app.route('/checkFlag')
def checkIsFlag():
    data = session['fileData']
    session['flagChecked'] = True
    if check_is_flag(data) == 1:
        session['flagChecked'] = False
        session['fileFlag'] = False
        session.pop('fileData', None)
        return "You Cannot Open flag ^~^"
    return redirect('/result')

@app.route('/result')
def res():
    if session.get('fileFlag') != True:
        return "File Already Closed"
    if session.get('flagChecked') != True:
        return "Check your data first"
    data = session['fileData']
    session['fileFlag'] = False
    session['flagChecked'] = False
    session.pop('fileData', None)
    return data


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
