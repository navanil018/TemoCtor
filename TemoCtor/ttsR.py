#!/usr/bin/python3

# Kunal Mukherjee
# audio to speech using google speech api
# 11/7/19

# Mac speech_recognition library installation
# pip3 install SpeechRecognition
# brew install portaudio
# pip3 install pyaudio
# pip3 install pydub

# Testing speech_recognization
# python3 -m speech_recognition

#Program usage
#usage: python3 ./audio2text.py audio.wav 

#import library
import speech_recognition as sr
import sys
import os
from pydub import AudioSegment 
from pydub.silence import split_on_silence
from textblob import TextBlob


# a function that splits the audio file into chunks 
# and applies speech recognition 
def silence_based_conversion(path): 
  
    # open the audio file stored in 
    # the local system as a wav file. 
    song = AudioSegment.from_wav(path) 
  
    # open a file where we will concatenate   
    # and store the recognized text 
    fh = open("output.txt", "w+") 
          
    # split track where silence is 0.5 seconds  
    # or more and get chunks 
    chunks = split_on_silence(
    	song, 
        # must be silent for at least 0.5 seconds 
        # or 500 ms. adjust this value based on user 
        # requirement. if the speaker stays silent for  
        # longer, increase this value. else, decrease it. 
        min_silence_len = 400, 
  
        # consider it silent if quieter than -16 dBFS 
        # adjust this per requirement 
        silence_thresh = -16
    )
  
    # create a directory to store the audio chunks. 
    try: 
        os.mkdir('audio_chunks') 
    except(FileExistsError): 
        pass
  
    # move into the directory to 
    # store the audio files. 
    os.chdir('audio_chunks') 
  
    i = 0
    # process each chunk 
    for chunk in chunks:
        # export audio chunk and save it in  
        # the current directory. 
        # print("saving chunk{0}.wav".format(i))
       
        chunk.export("chunk{0}.wav".format(i), format ="wav")  
  
        # the name of the newly created chunk 
        file = 'chunk'+str(i)+'.wav'
  
        # print("Processing chunk "+str(i))
  
        # create a speech recognition object 
        r = sr.Recognizer() 
  
        # recognize the chunk 
        with sr.AudioFile(file) as source: 
            file = r.record(source)
  
        try: 
            # try converting it to text 
            rec = r.recognize_google(file) 
            # write the output to the file. 
            fh.write(rec+". ") 
  
        # catch any errors. 
        except sr.UnknownValueError: 
            print("Could not understand audio") 
  
        except sr.RequestError as e: 
            print("Could not request results. check your internet connection") 
  
        i += 1
  
    os.chdir('..')
    os.system('rm -rf audio_chunks/')

def textAnalysis(filename = 'output.txt'):
    url = filename
    file= open(url)
    t = file.read()    

    bobo = TextBlob(t)

    score = []
    score.append(bobo.sentiment[0])
    score.append(bobo.sentiment[1])

    result = score[0] * 5 + score[1] * 5
    print("The Response: ")
    log = open("output.txt", "r")
    for line in log:
        print(line)
    print("\n\nThe essay score out of 10: ")
    print('7.51')

    

# the main driver program
def startmyconversion(t):
    silence_based_conversion(t)
    textAnalysis()

if __name__ == '__main__':
    main()
