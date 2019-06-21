from flask import Flask
from flask_ask import Ask, statement, question, session
import random
#import Datenbank

app = Flask(__name__)
app.secret_key = "hello"
ask = Ask(app, '/')
try:
    db = Datenbank()
    print "db connected"
except mysql.connector.errors.Erro as e:
    print "db can not be connected"

#Beginn des Gesprächs, nach Nutzer fragen
@ask.launch
def hello():
    return question('Hallo, wer bist du denn?')

#User erstellen und Grundstimmung erfragen, name ist Username
@ask.intent('UserIntent', convert={'name': str})
def createuser(name):
    session.attributes['session_key'] = 'how'
    #kein User mit dem Name vorhanden -> neuen erstellen
    if db.getUser(name) == null:
        db.createUser(name)
        session.attributes['userID'] = getUser(name)
        session.attributes['session_key'] = 'how'
        return question("Hallo {}, wie geht es dir heute?".format(name))
    #User vorhanden    
    else:
        session.attributes['userID'] = getUser(name)
        #überprüfen, ob heute bereits geredet wurde
        if db.getUserFeeling(session.attributes['userID']) == null:
            session.attributes['session_key'] = 'how'
            return question("Hallo {}, wie geht es dir heute?".format(name))
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

#Intent für alle positiven Antworten des Nutzers
@ask.intent('Yes')
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

#Intent für alle neutralen Antworten   
@ask.intent('Neutral')
def actionsNeutral():
    if session.attributes['session_key']=='how':
        session.attributes['session_key'] = 'maybetalkin'
        db.setUserFeeling(session.attribute['userID'], 0)
        return question("Hast du Lust zu reden?")

#Intent für alle schlechten Antworten
@ask.intent('No')
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
    #bei guter oder neutraler Laune ähnliche Reaktion, evtl ändern?
    if session.attributes['session_key'] == 'goodmood' || 'neutralmood':
        #Kein FutureStatus vorhanden, nachfragen!
        if db.getFutureStatus(session.attribute['userID'], action) == null:
            #Kein DoneStatus, keine Informationen vorliegen
            if db.getDoneStatus(session.attribute['userID'], action) == null:
                return question("Hat dir das Spaß gemacht?")
            #DoneStatus positiv -> hat Spaß gemacht
            elif db.getDoneStatus(session.attribute['userID'], action) == 1:
                return question("Du hattest Spaß, richtig?")
            #Done Status neutral
            elif db.getDoneStatus(session.attribute['userID'], action) == 0:               
                return question("Hattest du heute Spaß?")
            #DoneStatus negativ -> hat keinen Spaß gemacht
            else:
                return question("Du hattest keinen Spaß, oder?")
        #FutureStatus positiv -> Freude auf Aktivität
        elif db.getFutureStatus(session.attribute['userID'], action) == 1:
            return question("Du hast dich darauf gefreut, war es denn gut?")
        #FutureStatus neutral
        elif db.getFutureStatus(session.attribute['userID'], action) == 0:
            return question("War es so wie du erwartet hast?")
        #FutureStatus negativ -> Keine Freude auf Aktivität
        else:
            return question("Du hast dich nicht darauf gefreut, war es denn so schlecht?")
    #Schlechte Laune aus vorherigem Gespräch
    elif session.attributes['session_key'] == 'badmood':

#Intent bei ich werde..., ich muss...
@ask.intent('FutureActivityIntent', convert={'action': str})
def action(action):
    #Wenn aus vorherigem Gespräch gute Laune bestand
    if session.attributes['session_key'] == 'goodmood':
        db.getFutureStatus(session.attribute['userID'], action)

if __name__ == '__main__':
    app.run(debug=True)
