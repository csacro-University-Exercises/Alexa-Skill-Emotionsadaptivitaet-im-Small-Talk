from flask import Flask
from flask_ask import Ask, statement, question, session
import random
import mysql.connector
from datenbank import Datenbank

app = Flask(__name__)
app.secret_key = "hello"
ask = Ask(app, '/')
counter = 0
session.attributes['count'] = counter
try:
    db = Datenbank()
    print "db connected"
except mysql.connector.errors.Error as e:
    print "db can not be connected"

#Beginn des Gespraechs, nach Nutzer fragen
@ask.launch
def hello():
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
            return question("Dir geht es heute gut, oder?")
        elif db.getUserFeeling(session.attributes['userID']) == 0:
            session.attributes['session_key'] = 'how'
            return question("Wie geht es dir mittlerweile?")
        else:
            session.attributes['session_key'] = 'badhow'
            return question("Geht es dir immer noch schlecht?")

#Intent fuer alle positiven Antworten des Nutzers
@ask.intent('YesIntent')
def actionsGood():
    if session.attributes['session_key'] == 'how' :
        db.setUserFeeling(session.attribute['userID'], 1)
        session.attributes['session_key'] = 'goodmood'
        return question("Freut mich, dass es dir gut geht. Was machst du heute so?")
    elif session.attributes['session_key'] == 'badhow' :
        session.attributes['session_key'] = 'shutdown'
        db.setUserFeeling(session.attribute['userID'], -1)
        return question("Soll ich dich dann in Ruhe lassen?")
    elif session.attributes['session_key'] == 'shutdown':
        db.setUserFeeling(session.attribute['userID'], -1)
        return statement("Okay, dann lasse ich dich in Ruhe.")
    elif session.attributes['session_key'] == 'maybetalkin':
        session.attributes['session_key'] == 'neutralmood'
        return question("Okay, was machst du heute so?")
   

#Intent fuer alle neutralen Antworten   
@ask.intent('NeutralIntent')
def actionsNeutral():
    if session.attributes['session_key']=='how':
        session.attributes['session_key'] = 'maybetalkin'
        db.setUserFeeling(session.attribute['userID'], 0)
        return question("Hast du Lust zu reden?")

#Intent fuer alle schlechten Antworten
@ask.intent('NoIntent')
def actionsBad():
    if session.attributes['session_key']=='how':
        session.attributes['session_key'] = 'shutdown'
        db.setUserFeeling(session.attribute['userID'], -1)
        return question("Soll ich dich dann lieber in Ruhe lassen?")
    elif session.attributes['session_key'] == 'badhow':
        session.attributes['session_key'] == 'neutralmood'
        db.setUserFeeling(session.attribute['userID'], 1)
        return question("Freut mich, dass es dir besser geht. Was machst du denn heute so?")
    elif session.attributes['session_key'] == 'shutdown':
        session.attributes['session_key'] == 'badmood'
        db.setUserFeeling(session.attribute['userID'], -1)
        return question("Okay, was verdirbt dir denn dann deinen Tag?")
    elif session.attributes['session_key'] == 'maybetalkin':
        return statement("Okay, dann lasse ich dich in Ruhe")

#Intent bei ich habe...
@ask.intent('PastActivityIntent', convert={'action': str})
def action(action):
    session.attributes['session_key'] == 'fun'
    #bei guter oder neutraler Laune aehnliche Reaktion, evtl aendern?
    if session.attributes['session_key'] == 'goodmood' or 'neutralmood':
        #Kein FutureStatus vorhanden, nachfragen!
        if db.getFutureStatus(session.attribute['userID'], action) == None:
            #Kein DoneStatus, keine Informationen vorliegen
            if db.getDoneStatus(session.attribute['userID'], action) == None:
                return question("Hat dir das Spass gemacht?")
            #DoneStatus positiv -> hat Spass gemacht
            elif db.getDoneStatus(session.attribute['userID'], action) == 1:
                return question("Du hattest Spass, richtig?")
            #Done Status neutral
            elif db.getDoneStatus(session.attribute['userID'], action) == 0:               
                return question("Hattest du heute Spass?")
            #DoneStatus negativ -> hat keinen Spass gemacht
            else:
                return question("Du hattest keinen Spass, oder?")
        #FutureStatus positiv -> Freude auf Aktivitaet
        elif db.getFutureStatus(session.attribute['userID'], action) == 1:
            return question("Du hast dich darauf gefreut, war es denn gut?")
        #FutureStatus neutral
        elif db.getFutureStatus(session.attribute['userID'], action) == 0:
            return question("War es so wie du erwartet hast?")
        #FutureStatus negativ -> Keine Freude auf Aktivitaet
        else:
            return question("Du hast dich nicht darauf gefreut, war es denn so schlecht?")
    #Schlechte Laune aus vorherigem Gespraech
    elif session.attributes['session_key'] == 'badmood':
        print "fehlt noch"
#Kein FutureStatus vorhanden, nachfragen!
        if db.getFutureStatus(session.attribute['userID'], action) == None:
            #Kein DoneStatus, keine Informationen vorliegen
            if db.getDoneStatus(session.attribute['userID'], action) == None:
                return question("Das hat dir also keinen Spass gemacht?")
            #DoneStatus positiv -> hat Spass gemacht
            elif db.getDoneStatus(session.attribute['userID'], action) == 1:
                return question("Du hast vorher gesagt du hattest Spaß, stimmt das nicht mehr?")
            #Done Status neutral
            elif db.getDoneStatus(session.attribute['userID'], action) == 0:               
                return question("Hattest du heute dann keinen Spass?")
            #DoneStatus negativ -> hat keinen Spass gemacht
            else:
                return question("Also hat das dir den Tag verdorben?")
        #FutureStatus positiv -> Freude auf Aktivitaet
        elif db.getFutureStatus(session.attribute['userID'], action) == 1:
            return question("Du hast dich darauf gefreut, war es denn dann doch nicht gut?")
        #FutureStatus neutral
        elif db.getFutureStatus(session.attribute['userID'], action) == 0:
            return question("War es so wie du erwartet hast?")
        #FutureStatus negativ -> Keine Freude auf Aktivitaet
        else:
            return question("Du hast dich nicht darauf gefreut, also war es so schlecht?")
#Intent bei ich werde..., ich muss...
@ask.intent('FutureActivityIntent', convert={'action': str})
def action(action):
    #Wenn aus vorherigem Gespraech gute Laune bestand
    if session.attributes['session_key'] == 'goodmood':
        db.getFutureStatus(session.attribute['userID'], action)

#Vorschlaege fuer weitere Aktivitaeten
@ask.intent('SuggestionIntent')
def suggestion():    
    act = db.getFutureActivities
    if act[counter] != None:
        counter += 1
        session.attributes['count'] = counter
        if act[counter] != None:
            session.attributes['session_key'] = 'furthersuggestion'
            return question("Wie waere es mit {} . Soll ich dir eine weitere Aktivitaet vorschlagen, dann sag bitte Vorschlag".format(act[counter]))
        else:
            return statement("Wie waere es mit {} ?".format(act[counter]))
    else:
        return statement("Leider kann ich dir noch keine Aktivitaet vorschlagen")

if __name__ == '__main__':
    app.run(debug=True)
