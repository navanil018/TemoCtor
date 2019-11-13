from flask import Flask
from flask import abort
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
import speech_recognition as sr
from flask_socketio import SocketIO
import pyttsx3
import time

import threading
import time


    
    
engine = pyttsx3.init() # object creation
""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate                       #printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)                        #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female



import numpy as np
from scipy.io import wavfile
import os
import uuid

app = Flask(__name__)
import cloudconvert
api = cloudconvert.Api('')

i = 0
valt = "How was the Hackathon ?, Describe a challenging task of your life., What are some of your favorite projects. What made them uniques., This is a challenging task, How will you work on the skillset and what will you do to improve yourself. , How will you rate yourself in terms of your leadership skills."
valtarr = valt.split(',')
socketio = SocketIO(app)

def thread_function(name, t):
    engine.say(t)
    engine.runAndWait()
    engine.stop()
 



@app.route("/")
def welcome():
    x = threading.Thread(target=thread_function, args=(1,'Welcome! I am Proctor, Your automated Interviewer. I am here to help you prepare for your interview. Lets get started. Click on the Start button. How was the Hackathon ?',))
    x.start()
    return render_template("record.html", thismaval= valt)

@app.route("/start")
def start():
    response = make_response(redirect('/'))
    session_id = uuid.uuid4().hex
    response.set_cookie('session_id', session_id)
    return response

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['javascript_data']
    print(jsdata)

@app.route('/upload', methods=['POST'])
def upload():
    global i
    #session_id = request.cookies.get('session_id')
    #if not session_id:
    #    make_response('No session', 400)
    word = request.args.get('word')
    audio_data = request.data
    filename = str(i) + '_' + 'test' + '_'
    i+=1
    secure_name = filename
    # Left in for debugging purposes. If you comment this back in, the data
    # will be saved to the local file system.

    with open(secure_name + '.ogg', 'wb') as f:
        f.write(audio_data)
    try:
        process = api.convert({
        'inputformat': 'ogg',
        'outputformat': 'wav',
        'input': 'upload',
        'file': open(filename+'.ogg', 'rb')})
        process.wait() # wait until conversion finished
        process.download(filename + '.wav') # download output file
    except Exception as e:
        print(e)
    
    try:
        import ttsR
        print(ttsR.startmyconversion(filename + '.wav'))
    except Exception as e:
        print(e)

    return make_response('All good')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('testme')
def remove_ClientMapping(json, methods=['GET', 'POST']):
    print(json)
    time.sleep(3)


@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session['_csrf_token']
        if not token or token != request.args.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid.uuid4().hex
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token
app.secret_key = '123234mahandas'

if __name__ == '__main__':
    socketio.run(app, debug=True)
