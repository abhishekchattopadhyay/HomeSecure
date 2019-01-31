#!/usr/bin/python
'''
Author: Abhishek Chattopadhyay
Date:   26th Jan 2019
Business: The file proceses triggers from various sensors
'''
import RPi.GPIO as GPIO
import time
import json
import os

isArmed = False
isAlarmOn = False

BASEDIR=os.environ['HOMESECUREPATH']
if not len(BASEDIR): quit()

DEBUG = os.environ['DEBUG']

pirSensors=[]
pirSensivity = 2
relay=[]

def readConfigs():
    global pirSensors, relay, pirSensivity
    configF = os.path.join(os.path.join(BASEDIR,'HomeSecure/config'),'config.json')
    if not os.path.exists(configF): return False
    with open(configF) as f:
        data = json.load(f)
        pirSensors, relay, pirSensivity = data['sensors']['pir'], data['action']['relay'], data['sensors']['sensivity']['default']
        action_time = int(data['action']['time'])
        if action_time < 2: action_time = 10
        if DEBUG:
            print('pir_sensor_details: ', pirSensors)
            print('pir_sensivity: ', pirSensivity)
            print('relay_details: ', relay)
            print('act time: ', action_time)
        f.close()
    if len(pirSensors) and len(relay): return True
    return False

def setup():
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        global pirSensors, relay
        #Define sensor pins as an input pin
        for sensor in pirSensors+relay: GPIO.setup(sensor['gpio'],sensor['type'])
        return True
    except: 
        if DEBUG: 
            print ('passing even when setup is failed')
            return True
        return False

def readPIR():
    global pirSensors, pirSensivity
    # this is a generally low intellignet system so
    if not isArmed: return False
    pir_activity = [GPIO.LOW]*len(pirSensors)
    for idx in range(len(pinSensors)): 
        pir_activity[idx] = GPIO.INPUT(pirSensors[idx]['gpio'])
    if sum(pir_activity) >= pirSensivity: return True
    return False

def startRelay():
    global relay, isAlarmOn
    if isAlarmOn: return
    for re in relay: GPIO.OUTPUT(relay['gpio'],GPIO,HIGH)
    isAlarmOn = True

def take_action():
    # just go full throttle enable everything you got
    global take_action
    inActTime = 0
    while take_action > inActTime: 
        inActTime = inActTime + 1
        startRelay()

if __name__ == '__main__':
    if not readConfigs(): 
        if DEBUG: print('readConfigs failed')
        quit()
    if not setup():
        if DEBUG: print ('setup failed')
        quit()
    while True:
        time.sleep (10)
        if readPIR(): take_action()
        # schedule on off and action off
