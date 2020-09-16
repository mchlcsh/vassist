# coding=utf-8
# Dev: Michael Cash
# This is a virtual assistant to replace google home

import speech_recognition as sr
from phue import Bridge
import time
import pyttsx3
import logging

logging.basicConfig()

# initializes tts module
engine = pyttsx3.init()

# connects to Phillips Hue Bridge
myfile = open("ip.txt", "rt")
contents = myfile.read()
myfile.close()
b = Bridge(contents)
# b.connect() only run once

# sets time formats for vassist
current_time = time.localtime()
local_time = time.strftime('%H:%M', current_time)  # Hour/minute

text = ""
dim = "lights to"
count = "timer"


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening...")
        audio = r.listen(source)
        data = ""
    try:
        data = r.recognize_google(audio)
        global darr
        darr = data.split()
        print("You said: " + data)
        print (darr)
    except sr.UnknownValueError:
        print("I didn't understand")
    except sr.RequestError as e:
        print("Could not connect; {0}".format(e))
    return data

# Function takes string argument and coverts tts
def respond(audio_string):
    print(audio_string) # for debugging purposes
    engine.say(audio_string)
    engine.runAndWait()

# A function to handle Timer requests
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        cdown = '{:02d}:{:02d}'.format(mins, secs)
        print(cdown + "\r")
        time.sleep(1)
        t -= 1


# A function to check for wake word(s)
def wakeWord(wake):
    wake_words = ['okay raspberry']  # can add more wake words in array
    # Check to see if the users command/text contains a wake word
    for phrase in wake_words:
        if phrase in wake:
            return True


def virtual_assistant(data):
    if "what time is it" in data:
        listening = True
        respond(local_time)

    if "lights off" in data:
        listening = True
        b.set_light([1, 2], 'on', False)

    if "lights on" in data:
        listening = True
        b.set_light([1, 2], 'on', True)

    if data.__contains__(dim):
        dimnum = [int(s) for s in data.split() if s.isdigit()]
        dimnum = int(round(((float(dimnum[0]) / 100) * 254)))
        print(dimnum)
        b.set_light([1, 2], 'bri', dimnum)

    if data.__contains__(count):
        csec = "second"
        cmin = "minute"
        chour = "hour"
# initialize at zero, if no user input for denomination, will not affect timer calc
        thour = 0
        tmin = 0
        tsec = 0
# takes all inputs and calculates to seconds
        if chour in darr:
            thour = (darr.index(chour)) - 1
            thour = int(darr[thour]) * 3600
        if cmin in darr:
            tmin = (darr.index(cmin)) - 1
            tmin = int(darr[tmin]) * 60
        if csec in darr:
            tsec = (darr.index(csec)) - 1
            tsec = int(darr[tsec])
        timer = thour + tmin + tsec
        countdown(timer)
        respond("Timer Done")

# stops listening for commands, waits for wake word
    if "stop listening" in data:
        listening = False
        print("Listening stopped")


while True:
    wake = listen()

    if wakeWord(wake):
        listening = True
        while listening == True:
            data = listen()
            listening = virtual_assistant(data)
            listening = False
