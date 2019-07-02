#!/usr/bin/env python

from flask import Flask
from flask_ask import Ask, statement, question, session
import random
import mysql.connector
from datenbank import Datenbank

app = Flask(__name__)
app.secret_key = "hello"
ask = Ask(app, '/')
counter = 1

try:
    db = Datenbank()
    print "db connected"
except mysql.connector.errors.Error as e:
    print "db can not be connected"

#Beginn des Gespraechs, nach Nutzer fragen
@ask.launch
def hello():
	session.attributes['count'] = counter
	return question('Hallo, wer bist du denn?')
    
#User erstellen und Grundstimmung erfragen, name ist Username
@ask.intent('UserIntent', convert={'name': str})
def createuser(name):
    session.attributes['session_key'] = 'how'
    #kein User mit dem Name vorhanden -> neuen erstellen
    if db.getUser(name) == None:
        db.createUser(name)
        session.attributes['userID'] = db.getUser(name)
        session.attributes['session_key'] = 'how'
        return question("Hallo {}, wie geht es dir heute?".format(name))
    #User vorhanden    
    else:
        session.attributes['userID'] = db.getUser(name)
        #ueberpruefen, ob heute bereits geredet wurde
        if db.getUserFeeling(session.attributes['userID']) == None:
            session.attributes['session_key'] = 'how'
            return question("Hallo {}, schoen dich wieder zu sehen, wie geht es dir heute?".format(name))
        #Es wurde geredet -> Wie ist die Stimmung
        elif db.getUserFeeling(session.attributes['userID']) == 1:
            session.attributes['session_key'] = 'how'
            return question("Hallo {}, dir geht es heute gut, oder?".format(name))
        elif db.getUserFeeling(session.attributes['userID']) == 0:
            session.attributes['session_key'] = 'how'
            return question("Hallo {}, wie geht es dir mittlerweile?".format(name))
        else:
            session.attributes['session_key'] = 'badhow'
            return question("Hallo {}, geht es dir immer noch schlecht?".format(name))

#Intent fuer alle positiven Antworten des Nutzers
@ask.intent('YesIntent')
def actionsGood():
    if session.attributes['session_key'] == 'how' :
        db.setUserFeeling(session.attributes['userID'], 1)
        session.attributes['session_key'] = 'goodmood'
        return question("Freut mich, dass es dir gut geht. Was machst du heute so?")
    elif session.attributes['session_key'] == 'badhow' :
        session.attributes['session_key'] = 'shutdown'
        db.setUserFeeling(session.attributes['userID'], -1)
        return question("Soll ich dich dann in Ruhe lassen?")
    elif session.attributes['session_key'] == 'shutdown':
        db.setUserFeeling(session.attributes['userID'], -1)
        db.disconnectDatenbank()
        return statement("Okay, dann lasse ich dich in Ruhe.")
    elif session.attributes['session_key'] == 'maybetalkin':
        session.attributes['session_key'] == 'neutralmood'
        return question("Okay, was machst du heute sonst so?")

    elif session.attributes['session_key'] == 'futgoodnono':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Das freut mich. Was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futgoodno-1':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futgoodno0':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Das freut mich. Was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futgoodno1':
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        session.attributes['session_key'] == 'neutralmood'
        return question("Das freut mich. Was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futgood1':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futgood0':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futgood-1':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbad1':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbad0':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbad-1':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbadnono':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbadno1':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbadno0':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbadno-1':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgoodnono':
        session.attributes['session_key'] == 'goodmood'
        db.setDoneStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgoodno1':
        session.attributes['session_key'] == 'goodmood'
        db.setDoneStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgoodno0':
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 1)
        session.attributes['session_key'] == 'goodmood'
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgoodno-1':
        session.attributes['session_key'] == 'neutralmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgood1':
        session.attributes['session_key'] == 'neutralmood'
        db.moveFutureActivityToDone(session.
attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgood0':
        session.attributes['session_key'] == 'neutralmood'
        db.moveFutureActivityToDone(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgood-1':
        session.attributes['session_key'] == 'neutralmood'
        db.moveFutureActivityToDone(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbadnono':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbadno1':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbadno0':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbadno-1':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbad1':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbad0':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbad-1':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst so?")
   

#Intent fuer alle neutralen Antworten   
@ask.intent('NeutralIntent')
def actionsNeutral():
    if session.attributes['session_key']=='how':
        session.attributes['session_key'] = 'maybetalkin'
        db.setUserFeeling(session.attributes['userID'], 0)
        return question("Hast du Lust zu reden?")

    elif session.attributes['session_key'] == 'futgoodnono':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futgoodno-1':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futgoodno0':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futgoodno1':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futgood1':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futgood0':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futgood-1':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbad1':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbad0':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbad-1':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbadnono':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbadno1':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbadno0':
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        session.attributes['session_key'] == 'badmood'
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'futbadno-1':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgoodnono':
        session.attributes['session_key'] == 'goodmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgoodno1':
        session.attributes['session_key'] == 'goodmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgoodno0':
        session.attributes['session_key'] == 'goodmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgoodno-1':
        session.attributes['session_key'] == 'neutralmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgood1':
        session.attributes['session_key'] == 'neutralmood'
        db.moveFutureActivityToDone(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgood0':
        session.attributes['session_key'] == 'neutralmood'
        db.moveFutureActivityToDone(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastgood-1':
        session.attributes['session_key'] == 'neutralmood'
        db.moveFutureActivityToDone(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbadnono':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbadno1':
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 0)
        session.attributes['session_key'] == 'badmood'
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbadno0':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbadno-1':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbad1':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst so?")
    elif session.attributes['session_key'] == 'pastbad0':
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 0)
        session.attributes['session_key'] == 'badmood'
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastbad-1':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 0)
        return question("Okay, was machst du heute sonst noch?")

#Intent fuer alle schlechten Antworten
@ask.intent('NoIntent')
def actionsBad():
    if session.attributes['session_key']=='how':
        session.attributes['session_key'] = 'shutdown'
        db.setUserFeeling(session.attributes['userID'], -1)
        return question("Soll ich dich dann lieber in Ruhe lassen?")
    elif session.attributes['session_key'] == 'badhow':
        session.attributes['session_key'] == 'neutralmood'
        db.setUserFeeling(session.attributes['userID'], 1)
        return question("Freut mich, dass es dir besser geht. Was machst du denn heute so?")
    elif session.attributes['session_key'] == 'shutdown':
        session.attributes['session_key'] == 'badmood'
        db.setUserFeeling(session.attributes['userID'], -1)
        return question("Okay, was verdirbt dir denn dann deinen Tag?")
    elif session.attributes['session_key'] == 'maybetalkin':
        db.disconnectDatenbank()
        return statement("Okay, dann lasse ich dich in Ruhe")


    elif session.attributes['session_key'] == 'futgoodnono':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futgoodno-1':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futgoodno0':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Das ist schade. Was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futgoodno1':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futgood1':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Schade, dass du dich nicht mehr freust. Was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futgood0':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futgood-1':
        session.attributes['session_key'] == 'neutralmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Schoen, dass du deine Meinung geaendert hast. Was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futbad1':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futbad0':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futbad-1':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futbadnono':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futbadno1':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futbadno0':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Schade, aber was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'futbadno-1':
        session.attributes['session_key'] == 'badmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastgoodnono':
        session.attributes['session_key'] == 'goodmood'
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastgoodno1':
        session.attributes['session_key'] == 'goodmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastgoodno0':
        session.attributes['session_key'] == 'goodmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastgoodno-1':
        session.attributes['session_key'] == 'neutralmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastgood1':
        session.attributes['session_key'] == 'neutralmood'
        db.moveFutureActivityToDone(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastgood0':
        session.attributes['session_key'] == 'neutralmood'
        db.moveFutureActivityToDone(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastgood-1':
        session.attributes['session_key'] == 'neutralmood'
        db.moveFutureActivityToDone(session.
attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastbadnono':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastbadno1':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastbadno0':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastbadno-1':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastbad1':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastbad0':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], -1)
        return question("Okay, was machst du heute sonst noch?")
    elif session.attributes['session_key'] == 'pastbad-1':
        session.attributes['session_key'] == 'badmood'
        db.setDoneStatus(session.
attributes['userID'], session.attributes['action'], 1)
        return question("Okay, was machst du heute sonst noch?")

#Intent bei ich habe...
@ask.intent('PastActivityIntent', convert={'action': str})
def action(action):
    session.attributes['session_key'] == 'fun'
    session.attributes['action'] = action
    #bei guter oder neutraler Laune aehnliche Reaktion, evtl aendern?
    if session.attributes['session_key'] == 'goodmood' or 'neutralmood':
        #Kein FutureStatus vorhanden, nachfragen!
        if db.getFutureStatus(session.attributes['userID'], action) == None:
            #Kein DoneStatus, keine Informationen vorliegen
            if db.getDoneStatus(session.attributes['userID'], action) == None:
                session.attributes['session_key'] = 'pastgoodnono'
                return question("Hat dir das Spass gemacht?")
            #DoneStatus positiv -> hat Spass gemacht
            elif db.getDoneStatus(session.attributes['userID'], action) == 1:
                session.attributes['session_key'] = 'pastgoodno1'
                return question("Du hattest Spass, richtig?")
            #Done Status neutral
            elif db.getDoneStatus(session.attributes['userID'], action) == 0:         
                session.attributes['session_key'] = 'pastgoodno0'      
                return question("Hattest du heute Spass?")
            #DoneStatus negativ -> hat keinen Spass gemacht
            else:
                session.attributes['session_key'] = 'pastgoodno-1'
                return question("Du hattest keinen Spass, oder?")
        #FutureStatus positiv -> Freude auf Aktivitaet
        elif db.getFutureStatus(session.attributes['userID'], action) == 1:
            session.attributes['session_key'] = 'pastgood1'
            return question("Du hast dich darauf gefreut, war es denn gut?")
        #FutureStatus neutral
        elif db.getFutureStatus(session.attributes['userID'], action) == 0:
            session.attributes['session_key'] = 'pastgood0'
            return question("War es nur so la la?")
        #FutureStatus negativ -> Keine Freude auf Aktivitaet
        else:
            session.attributes['session_key'] = 'pastgood-1'
            return question("Du hast dich nicht darauf gefreut, war es denn so schlecht?")
    #Schlechte Laune aus vorherigem Gespraech
    elif session.attributes['session_key'] == 'badmood':
        #Kein FutureStatus vorhanden, nachfragen!
        if db.getFutureStatus(session.attributes['userID'], action) == None:
            #Kein DoneStatus, keine Informationen vorliegen
            if db.getDoneStatus(session.attributes['userID'], action) == None:
                session.attributes['session_key'] = 'pastbadnono'
                return question("Das hat dir also keinen Spass gemacht?")
            #DoneStatus positiv -> hat Spass gemacht
            elif db.getDoneStatus(session.attributes['userID'], action) == 1:
                session.attributes['session_key'] = 'pastbadno1'
                return question("Du hast vorher gesagt du hattest Spass, stimmt das nicht mehr?")
            #Done Status neutral
            elif db.getDoneStatus(session.attributes['userID'], action) == 0:           
                session.attributes['session_key'] = 'pastbadno0'    
                return question("Hattest du heute dann keinen Spass?")
            #DoneStatus negativ -> hat keinen Spass gemacht
            else:
                session.attributes['session_key'] = 'pastbadno-1'
                return question("Also hat das dir den Tag verdorben?")
        #FutureStatus positiv -> Freude auf Aktivitaet
        elif db.getFutureStatus(session.attributes['userID'], action) == 1:
            session.attributes['session_key'] = 'pastbad1'
            return question("Du hast dich darauf gefreut, war es denn dann doch nicht gut?")
        #FutureStatus neutral
        elif db.getFutureStatus(session.attributes['userID'], action) == 0:
            session.attributes['session_key'] = 'pastbad0'
            return question("War es so la la?")
        #FutureStatus negativ -> Keine Freude auf Aktivitaet
        else:
            session.attributes['session_key'] = 'pastbad-1'
            return question("Du hast dich nicht darauf gefreut, also war es so schlecht?")

#Intent bei ich werde..., ich muss...
@ask.intent('FutureActivityIntent', convert={'action': str})
def action(action):
    #Wenn aus vorherigem Gespraech gute Laune bestand
    session.attributes['action'] = action
    if session.attributes['session_key'] == 'goodmood':
        if db.getFutureStatus(session.attributes['userID'], action) == 1:
            session.attributes['session_key'] = 'futgood1'
            return question("Du freust dich darauf, oder?")
        elif db.getFutureStatus(session.attributes['userID'], action) == 0:
            session.attributes['session_key'] = 'futgood0'
            return question("Freust du dich jetzt?")
        elif db.getFutureStatus(session.attributes['userID'], action) == -1:
            session.attributes['session_key'] = 'futgood-1'
            return question("Du freust dich nicht darauf, oder?")
        else:
            if db.getDoneStatus(session.attributes['userID'], action) == 1:
                session.attributes['session_key'] = 'futgoodno1'
                return question("Normalerweise freust du dich darauf, heute auch?")
            elif db.getDoneStatus(session.attributes['userID'], action) == 0:
                session.attributes['session_key'] = 'futgoodno0'
                return question("Wie stehst du heute dazu?")
            elif db.getDoneStatus(session.attributes['userID'], action) == -1:
                session.attributes['session_key'] = 'futgoodno-1'
                return question("Du freust dich normal nicht darauf, freust du dich heute?")
            else:
                session.attributes['session_key'] = 'futgoodnono'
                return question("Freust du dich?")
    #Wenn aus vorherigem Gespraech schlechte Laune bestand
    elif session.attributes['session_key'] == 'badmood':
        if db.getFutureStatus(session.attributes['userID'], action) == 1:
            session.attributes['session_key'] = 'futbad1'
            return question("Freust du dich nicht mehr?")
        elif db.getFutureStatus(session.attributes['userID'], action) == 0:
            session.attributes['session_key'] = 'futbad0'
            return question("Hast du jetzt gar keine Lust mehr?")
        elif db.getFutureStatus(session.attributes['userID'], action) == -1:
            session.attributes['session_key'] = 'futbad-1'
            return question("Du freust dich sicher nicht darauf, oder?")
        else:
            if db.getDoneStatus(session.attributes['userID'], action) == 1:
                session.attributes['session_key'] = 'futbadno1'
                return question("Normalerweise freust du dich darauf, heute auch?")
            elif db.getDoneStatus(session.attributes['userID'], action) == 0:
                session.attributes['session_key'] = 'futbadno0'
                return question("Freust du dich heute?")
            elif db.getDoneStatus(session.attributes['userID'], action) == -1:
                session.attributes['session_key'] = 'futbadno-1'
                return question("Du freust dich normal nicht darauf, heute bestimmt auch nicht?")
            else:
                session.attributes['session_key'] = 'futbadnono'
                return question("Freust du dich?")

#Vorschlaege fuer weitere Aktivitaeten
# Nichts als Antwort hinzufuegen!!!
@ask.intent('SuggestionIntent')
def suggestion():   
    global counter 
    act = db.getActivity(session.attributes['userID'], counter)
    if act != None:
        counter += 1
        session.attributes['count'] = counter
        if db.getActivity(session.attributes['userID'], counter) != None:
            session.attributes['session_key'] = 'furthersuggestion'
            return question("Wie waere es mit {} . Soll ich dir eine weitere Aktivitaet vorschlagen, dann sag bitte Vorschlag oder Ende zum Beenden".format(act))
        else:
            db.disconnectDatenbank()
            return statement("Du koenntest {}".format(act))
    else:
        db.disconnectDatenbank()
        return statement("Leider kann ich dir noch keine Aktivitaet vorschlagen")

@ask.intent('TellFutureIntent')
def tell():
    activities = db.getFutureActivities(session.attributes['userID'])
    if activities == None:
        return question("Du hast heute noch nichts geplant")
    else:
        liste = "Du hast heute "
        for i in range(0, len(activities)):
            if i == (len(activities) -2):
                liste += activities[i][0]
                liste += " und "       
            elif i == (len(activities) - 1):
                liste += activities[i][0]
            else:
                liste += activities[i][0]
                liste += ", "
        liste += " geplant"
        return question(liste)

@ask.intent('AMAZON.CancelIntent')
def cancel():
    db.disconnectDatenbank()
    return statement('Okay ich beende mich jetzt')

if __name__ == '__main__':
    app.run(debug=True)
