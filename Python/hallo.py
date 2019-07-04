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

db = Datenbank()

@ask.launch
def hello():
    print("launch")
    try:
        db.connectDatenbank()
        print "db (re)connected"
        session.attributes['count'] = counter
        return question('Hallo, wer bist du denn?')
    except mysql.connector.errors.Error as e:
        print "db can not be (re)connected"

@ask.intent('AMAZON.StopIntent')
def cancel():
    print("cancel")
    db.disconnectDatenbank()
    print("db disconnected")
    return statement('Okay ich beende mich jetzt')

@ask.intent('UserIntent', convert={'name': str})
def createuser(name):
    print("UserIntent")
    session.attributes['session_key'] = 'how'
    userId = db.getUser(name)
    if userId == None:
        session.attributes['userID'] = db.createUser(name)
        session.attributes['session_key'] = 'how'
        return question("Hallo {}, wie geht es dir heute?".format(name))
    else:
        session.attributes['userID'] = userId
        userFeeling = db.getUserFeeling(userId)
        userFeelingKeySwitcher = {
            1: 'how',
            0: 'how',
            -1: 'badhow'
        }
        userFeelingAnswSwitcher = {
            1: "Hallo {}, dir geht es heute gut, oder?",
            0: "Hallo {}, wie geht es dir mittlerweile?",
            -1: "Hallo {}, geht es dir immer noch schlecht?"
        }

        session.attributes['session_key'] = userFeelingKeySwitcher.get(userFeeling, 'how')

        answ = userFeelingAnswSwitcher.get(userFeeling, "Hallo {}, schoen dich wieder zu sehen, wie geht es dir heute?")
        return question(str(answ).format(name))

@ask.intent('YesIntent')
def actionsGood():
    print("YesIntent")
    sessionkey = session.attributes['session_key']
    sessionKeyKeySwitcher = {
        'how': 'goodmood',
        'badhow': 'shutdown',
        'shutdown': 'shutdown',
        'maybetalkin': 'neutralmood',
        'futgoodnono': 'neutralmood',
        'futgoodnono-1': 'neutralmood',
        'futgoodno0': 'neutralmood',
        'futgoodno1': 'neutralmood',
        'futgood1': 'neutralmood',
        'futgood0': 'neutralmood',
        'futgood-1': 'neutralmood',
        'futbad1': 'badmood',
        'futbad0': 'badmood',
        'futbad-1': 'badmood',
        'futbadnono': 'badmood',
        'futbadno1': 'badmood',
        'futbadno0': 'badmood',
        'futbadno-1': 'badmood',
        'pastgoodnono': 'goodmood',
        'pastgoodno1': 'goodmood',
        'pastgoodno0': 'goodmood',
        'pastgoodno-1': 'neutralmood',
        'pastgood1': 'neutralmood',
        'pastgood0': 'neutralmood',
        'pastgood-1': 'neutralmood',
        'pastbadnono': 'badmood',
        'pastbadno1': 'badmood',
        'pastbadno0': 'badmood',
        'pastbadno-1': 'badmood',
        'pastbad1': 'badmood',
        'pastbad0': 'badmood',
        'pastbad-1': 'badmood'
    }
    sessionKeyFeelingSwitcher = {
        'how': 1,
        'badhow': -1,
        'shutdown': -1,
        'maybetalkin': 0
    }
    sessionKeyFuturestatusSwitcher = {
        'futgoodnono': 1,
        'futgoodnono-1': 1,
        'futgoodno0': 1,
        'futgoodno1': 1,
        'futgood1': 1,
        'futgood0': 1,
        'futgood-1': -1,
        'futbad1': -1,
        'futbad0': -1,
        'futbad-1': 1,
        'futbadnono': 1,
        'futbadno1': 1,
        'futbadno0': 1,
        'futbadno-1': -1
    }
    sessionKeyDonestatusSwitcher = {
        'pastgoodnono': 1,
        'pastgoodno1': 1,
        'pastgoodno0': 1,
        'pastgoodno-1': 1,
        'pastbadnono': 1,
        'pastbadno1': 1,
        'pastbadno0': 1,
        'pastbadno-1': -1,
        'pastbad1': 1,
        'pastbad0': 0,
        'pastbad-1': -1
    }
    sessionKeyFuture2DoneSwitcher = {
        'pastgood1': 1,
        'pastgood0': 0,
        'pastgood-1': -1,
    }
    sessionKeyAnswSwitcher = {
        'how': "Freut mich, dass es dir gut geht. Was machst du heute so?",
        'badhow': "Soll ich dich dann in Ruhe lassen?",
        'shutdown': "Okay, dann lasse ich dich in Ruhe.",
        'maybetalkin': "Okay, was machst du heute sonst so?",
        'futgoodnono': "Das freut mich. Was machst du heute sonst so?",
        'futgoodnono-1': "Okay, was machst du heute sonst so?",
        'futgoodno0': "Das freut mich. Was machst du heute sonst so?",
        'futgoodno1': "Das freut mich. Was machst du heute sonst so?",
        'futgood1': "Okay, was machst du heute sonst so?",
        'futgood0': "Okay, was machst du heute sonst so?",
        'futgood-1': "Okay, was machst du heute sonst so?",
        'futbad1': "Okay, was machst du heute sonst so?",
        'futbad0': "Okay, was machst du heute sonst so?",
        'futbad-1': "Okay, was machst du heute sonst so?",
        'futbadnono': "Okay, was machst du heute sonst so?",
        'futbadno1': "Okay, was machst du heute sonst so?",
        'futbadno0': "Okay, was machst du heute sonst so?",
        'futbadno-1': "Okay, was machst du heute sonst so?",
        'pastgoodnono': "Okay, was machst du heute sonst so?",
        'pastgoodno1': "Okay, was machst du heute sonst so?",
        'pastgoodno0': "Okay, was machst du heute sonst so?",
        'pastgoodno-1': "Okay, was machst du heute sonst so?",
        'pastgood1': "Okay, was machst du heute sonst so?",
        'pastgood0': "Okay, was machst du heute sonst so?",
        'pastgood-1': "Okay, was machst du heute sonst so?",
        'pastbadnono': "Okay, was machst du heute sonst so?",
        'pastbadno1': "Okay, was machst du heute sonst so?",
        'pastbadno0': "Okay, was machst du heute sonst so?",
        'pastbadno-1': "Okay, was machst du heute sonst so?",
        'pastbad1': "Okay, was machst du heute sonst so?",
        'pastbad0': "Okay, was machst du heute sonst so?",
        'pastbad-1': "Okay, was machst du heute sonst so?"


    }

    session.attributes['session_key'] = sessionKeyKeySwitcher.get(sessionkey, 'how')

    feeling = sessionKeyFeelingSwitcher.get(sessionkey, None)
    futurestatus = sessionKeyFuturestatusSwitcher.get(sessionkey, None)
    donestatus = sessionKeyDonestatusSwitcher.get(sessionkey, None)
    future2done = sessionKeyFuture2DoneSwitcher.get(sessionkey, None)
    if(feeling != None):
        db.setUserFeeling(session.attributes['userID'], feeling)
    if(futurestatus != None):
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], futurestatus)
    if(donestatus != None):
        db.setDoneStatus(session.attributes['userID'], session.attributes['action'], donestatus)
    if(future2done != None):
        db.moveFutureActivityToDone(session.attributes['userID'], session.attributes['action'], future2done)

    answ = sessionKeyAnswSwitcher.get(sessionkey, "Was machst du heute sonst so?")
    if(session.attributes['session_key'] == 'shutdown'):
        db.disconnectDatenbank()
        return statement(answ)
    else:
        return question(answ)

@ask.intent('NeutralIntent')
def actionsNeutral():
    print("NeutralIntent")
    sessionkey = session.attributes['session_key']
    sessionKeyKeySwitcher = {
        'how': 'maybetalkin',
        'futgoodnono': 'neutralmood',
        'futgoodno-1': 'neutralmood',
        'futgoodno0': 'neutralmood',
        'futgoodno1': 'neutralmood',
        'futgood1': 'neutralmood',
        'futgood0': 'neutralmood',
        'futgood-1': 'neutralmood',
        'futbad1': 'badmood',
        'futbad0': 'badmood',
        'futbad-1': 'badmood',
        'futbadnono': 'badmood',
        'futbadno1': 'badmood',
        'futbadno0': 'badmood',
        'futbadno-1': 'badmood',
        'pastgoodnono': 'goodmood',
        'pastgoodno1': 'goodmood',
        'pastgoodno0': 'goodmood',
        'pastgoodno-1': 'neutralmood',
        'pastgood1': 'neutralmood',
        'pastgood0': 'neutralmood',
        'pastgood-1': 'neutralmood',
        'pastbadnono': 'badmood',
        'pastbadno1': 'badmood',
        'pastbadno0': 'badmood',
        'pastbadno-1': 'badmood',
        'pastbad1': 'badmood',
        'pastbad0': 'badmood',
        'pastbad-1': 'badmood'
    }
    sessionKeyFeelingSwitcher = {
        'how': 0
    }
    sessionKeyFuturestatusSwitcher = {
        'futgoodnono': 0,
        'futgoodno-1': 0,
        'futgoodno0': 0,
        'futgoodno1': 0,
        'futgood1': 0,
        'futgood0': 0,
        'futgood-1': 0,
        'futbad1': 0,
        'futbad0': 0,
        'futbad-1': 0,
        'futbadnono': 0,
        'futbadno1': 0,
        'futbadno0': 0,
        'futbadno-1': 0
    }
    sessionKeyDonestatusSwitcher = {
        'pastgoodnono': 0,
        'pastgoodno1': 0,
        'pastgoodno0': 0,
        'pastgoodno-1': 0,
        'pastbadnono': 0,
        'pastbadno1': 0,
        'pastbadno0': 0,
        'pastbadno-1': 0,
        'pastbad1': 0,
        'pastbad0': 0,
        'pastbad-1': 0
    }
    sessionKeyFuture2DoneSwitcher = {
        'pastgood1': 0,
        'pastgood0': 0,
        'pastgood-1': 0
    }
    sessionKeyAnswSwitcher = {
        'how': "Hast du Lust zu reden?",
        'futgoodnono': "Okay, was machst du heute sonst so?",
        'futgoodno-1': "Okay, was machst du heute sonst so?",
        'futgoodno0': "Okay, was machst du heute sonst so?",
        'futgoodno1': "Okay, was machst du heute sonst so?",
        'futgood1': "Okay, was machst du heute sonst so?",
        'futgood0': "Okay, was machst du heute sonst so?",
        'futgood-1': "Okay, was machst du heute sonst so?",
        'futbad1': "Okay, was machst du heute sonst so?",
        'futbad0': "Okay, was machst du heute sonst so?",
        'futbad-1': "Okay, was machst du heute sonst so?",
        'futbadnono': "Okay, was machst du heute sonst so?",
        'futbadno1': "Okay, was machst du heute sonst so?",
        'futbadno0': "Okay, was machst du heute sonst so?",
        'futbadno-1': "Okay, was machst du heute sonst so?",
        'pastgoodnono': "Okay, was machst du heute sonst so?",
        'pastgoodno1': "Okay, was machst du heute sonst so?",
        'pastgoodno0': "Okay, was machst du heute sonst so?",
        'pastgoodno-1': "Okay, was machst du heute sonst so?",
        'pastgood1': "Okay, was machst du heute sonst so?",
        'pastgood0': "Okay, was machst du heute sonst so?",
        'pastgood-1': "Okay, was machst du heute sonst so?",
        'pastbadnono': "Okay, was machst du heute sonst so?",
        'pastbadno1': "Okay, was machst du heute sonst so?",
        'pastbadno0': "Okay, was machst du heute sonst so?",
        'pastbadno-1': "Okay, was machst du heute sonst so?",
        'pastbad1': "Okay, was machst du heute sonst so?",
        'pastbad0': "Okay, was machst du heute sonst so?",
        'pastbad-1': "Okay, was machst du heute sonst so?"
    }

    session.attributes['session_key'] = sessionKeyKeySwitcher.get(sessionkey, 'how')

    feeling = sessionKeyFeelingSwitcher.get(sessionkey, None)
    futurestatus = sessionKeyFuturestatusSwitcher.get(sessionkey, None)
    donestatus = sessionKeyDonestatusSwitcher.get(sessionkey, None)
    future2done = sessionKeyFuture2DoneSwitcher.get(sessionkey, None)
    if (feeling != None):
        db.setUserFeeling(session.attributes['userID'], feeling)
    if (futurestatus != None):
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], futurestatus)
    if (donestatus != None):
        db.setDoneStatus(session.attributes['userID'], session.attributes['action'], donestatus)
    if (future2done != None):
        db.moveFutureActivityToDone(session.attributes['userID'], session.attributes['action'], future2done)

    answ = sessionKeyAnswSwitcher.get(sessionkey, "Was machst du heute sonst so?")
    return question(answ)

@ask.intent('NoIntent')
def actionsBad():
    print("NoIntent")
    sessionkey = session.attributes['session_key']
    sessionKeyKeySwitcher = {
        'how': 'shutdown',
        'badhow': 'neutralmood',
        'shutdown': 'badmood',
        'futgoodnono': 'neutralmood',
        'futgoodno-1': 'neutralmood',
        'futgoodno0': 'neutralmood',
        'futgoodno1': 'neutralmood',
        'futgood1': 'neutralmood',
        'futgood0': 'neutralmood',
        'futgood-1': 'neutralmood',
        'futbad1': 'badmood',
        'futbad0': 'badmood',
        'futbad-1': 'badmood',
        'futbadnono': 'badmood',
        'futbadno1': 'badmood',
        'futbadno0': 'badmood',
        'futbadno-1': 'badmood',
        'pastgoodnono': 'goodmood',
        'pastgoodno1': 'goodmood',
        'pastgoodno0': 'goodmood',
        'pastgoodno-1': 'neutralmood',
        'pastgood1': 'neutralmood',
        'pastgood0': 'neutralmood',
        'pastgood-1': 'neutralmood',
        'pastbadnono': 'badmood',
        'pastbadno1': 'badmood',
        'pastbadno0': 'badmood',
        'pastbadno-1': 'badmood',
        'pastbad1': 'badmood',
        'pastbad0': 'badmood',
        'pastbad-1': 'badmood'
    }
    sessionKeyFeelingSwitcher = {
        'how': -1,
        'badhow': 1,
    }
    sessionKeyFuturestatusSwitcher = {
        'futgoodnono': -1,
        'futgoodno-1': -1,
        'futgoodno0': -1,
        'futgoodno1': -1,
        'futgood1': -1,
        'futgood0': -1,
        'futgood-1': -1,
        'futbad1': 1,
        'futbad0': 1,
        'futbad-1': -1,
        'futbadnono': -1,
        'futbadno1': -1,
        'futbadno0': -1,
        'futbadno-1': 1
    }
    sessionKeyDonestatusSwitcher = {
        'pastgoodnono': -1,
        'pastgoodno1': -1,
        'pastgoodno0': -1,
        'pastgoodno-1': -1,
        'pastbadnono': -1,
        'pastbadno1': -1,
        'pastbadno0': -1,
        'pastbadno-1': 1,
        'pastbad1': -1,
        'pastbad0': -1,
        'pastbad-1': 1
    }
    sessionKeyFuture2DoneSwitcher = {
        'pastgood1': -1,
        'pastgood0': -1,
        'pastgood-1': 1
    }
    sessionKeyAnswSwitcher = {
        'how': "Soll ich dich dann lieber in Ruhe lassen?",
        'badhow': "Freut mich, dass es dir besser geht. Was machst du denn heute so?",
        'shutdown': "Okay, was verdirbt dir denn dann deinen Tag?",
        'maybetalkin': "Okay, dann lasse ich dich in Ruhe",
        'futgoodnono': "Okay, was machst du heute sonst noch?",
        'futgoodno-1': "Okay, was machst du heute sonst noch?",
        'futgoodno0': "Das ist schade. Was machst du heute sonst noch?",
        'futgoodno1': "Okay, was machst du heute sonst noch?",
        'futgood1': "Schade, dass du dich nicht mehr freust. Was machst du heute sonst noch?",
        'futgood0': "Okay, was machst du heute sonst noch?",
        'futgood-1': "Schoen, dass du deine Meinung geaendert hast. Was machst du heute sonst noch?",
        'futbad1': "Okay, was machst du heute sonst noch?",
        'futbad0': "Schade, aber was machst du heute sonst noch?",
        'futbad-1': "Okay, was machst du heute sonst noch?",
        'futbadnono': "Okay, was machst du heute sonst noch?",
        'futbadno1': "Okay, was machst du heute sonst noch?",
        'futbadno0': "Okay, was machst du heute sonst noch?",
        'futbadno-1': "Okay, was machst du heute sonst noch?",
        'pastgoodnono': "Okay, was machst du heute sonst noch?",
        'pastgoodno1': "Okay, was machst du heute sonst noch?",
        'pastgoodno0': "Okay, was machst du heute sonst noch?",
        'pastgoodno-1': "Okay, was machst du heute sonst noch?",
        'pastgood1': "Okay, was machst du heute sonst noch?",
        'pastgood0': "Okay, was machst du heute sonst noch?",
        'pastgood-1': "Okay, was machst du heute sonst noch?",
        'pastbadnono': "Okay, was machst du heute sonst noch?",
        'pastbadno1': "Okay, was machst du heute sonst noch?",
        'pastbadno0': "Okay, was machst du heute sonst noch?",
        'pastbadno-1': "Okay, was machst du heute sonst noch?",
        'pastbad1': "Okay, was machst du heute sonst noch?",
        'pastbad0': "Okay, was machst du heute sonst noch?",
        'pastbad-1': "Okay, was machst du heute sonst noch?"
    }

    session.attributes['session_key'] = sessionKeyKeySwitcher.get(sessionkey, 'how')

    feeling = sessionKeyFeelingSwitcher.get(sessionkey, None)
    futurestatus = sessionKeyFuturestatusSwitcher.get(sessionkey, None)
    donestatus = sessionKeyDonestatusSwitcher.get(sessionkey, None)
    future2done = sessionKeyFuture2DoneSwitcher.get(sessionkey, None)
    if (feeling != None):
        db.setUserFeeling(session.attributes['userID'], feeling)
    if (futurestatus != None):
        db.setFutureStatus(session.attributes['userID'], session.attributes['action'], futurestatus)
    if (donestatus != None):
        db.setDoneStatus(session.attributes['userID'], session.attributes['action'], donestatus)
    if (future2done != None):
        db.moveFutureActivityToDone(session.attributes['userID'], session.attributes['action'], future2done)

    answ = sessionKeyAnswSwitcher.get(sessionkey, "Was machst du heute sonst so?")
    if (session.attributes['session_key'] == 'maybetalkin'):
        db.disconnectDatenbank()
        return statement(answ)
    else:
        return question(answ)

@ask.intent('PastActivityIntent', convert={'action': str})
def action(action):
    print("PastActivityIntent")
    session.attributes['action'] = action

    if session.attributes['session_key'] == 'badmood':
        futurestatus = db.getFutureStatus(session.attributes['userID'], action)
        if (futurestatus != None):
            futurestatusKeySwitcher = {
                1: 'pastbad1',
                0: 'pastbad0',
                -1: 'pastbad-1'
            }
            futurestatusAnswSwitcher = {
                1: "Du hast dich eigentlich darauf gefreut, war es schlecht?",
                0: "War es so la la?",
                -1: "Du hast dich nicht darauf gefreut, also war es schlecht?"
            }

            session.attributes['session_key'] = futurestatusKeySwitcher.get(futurestatus, 'pastbadnono')
            answ = futurestatusAnswSwitcher.get(futurestatus, "Das hat dir also keinen Spass gemacht?")
        else:
            donestatus = db.getDoneStatus(session.attributes['userID'], action)
            donestatusKeySwitcher = {
                1: 'pastbadno1',
                0: 'pastbadno0',
                -1: 'pastbadno-1'
            }
            donestatusAnswSwitcher = {
                1: "Normalerweise macht dir das aber Spass, heute nicht?",
                0: "Hattest du heute keinen Spass?",
                -1: "Also hat das dir den Tag verdorben?"
            }

            session.attributes['session_key'] = donestatusKeySwitcher.get(donestatus, 'pastbadnono')
            answ = donestatusAnswSwitcher.get(donestatus, "Das hat dir also keinen Spass gemacht?")
        return question(answ)
    else:
        futurestatus = db.getFutureStatus(session.attributes['userID'], action)
        if (futurestatus != None):
            futurestatusKeySwitcher = {
                1: 'pastgood1',
                0: 'pastgood0',
                -1: 'pastgood-1'
            }
            futurestatusAnswSwitcher = {
                1: "Du hast dich darauf gefreut, war es denn gut?",
                0: "War es nur so la la?",
                -1: "Du hast dich nicht darauf gefreut, war es denn so schlecht?"
            }

            session.attributes['session_key'] = futurestatusKeySwitcher.get(futurestatus, 'pastgoodnono')
            answ = futurestatusAnswSwitcher.get(futurestatus, "Hat dir das Spass gemacht?")
        else:
            donestatus = db.getDoneStatus(session.attributes['userID'], action)
            donestatusKeySwitcher = {
                1: 'pastgoodno1',
                0: 'pastgoodno0',
                -1: 'pastgoodno-1'
            }
            donestatusAnswSwitcher = {
                1: "Du hattest Spass, richtig?",
                0: "Hattest du heute Spass?",
                -1: "Du hattest keinen Spass, oder?"
            }

            session.attributes['session_key'] = donestatusKeySwitcher.get(donestatus, 'pastgoodnono')
            answ = donestatusAnswSwitcher.get(donestatus, "Hat dir das Spass gemacht?")
        return question(answ)

@ask.intent('FutureActivityIntent', convert={'action': str})
def action(action):
    print("FutureActivityIntent")
    session.attributes['action'] = action

    if session.attributes['session_key'] == 'badmood':
        futurestatus = db.getFutureStatus(session.attributes['userID'], action)
        if (futurestatus != None):
            futurestatusKeySwitcher = {
                1: 'futbad1',
                0: 'futbad0',
                -1: 'futbad-1'
            }
            futurestatusAnswSwitcher = {
                1: "Freust du dich nicht mehr?",
                0: "Hast du jetzt keine Lust mehr darauf?",
                -1: "Du freust dich sicher nicht darauf, oder?"
            }

            session.attributes['session_key'] = futurestatusKeySwitcher.get(futurestatus, 'badmood')
            answ = futurestatusAnswSwitcher.get(futurestatus, "Das ist schade. Was machst du sonst so?")
        else:
            donestatus = db.getDoneStatus(session.attributes['userID'], action)
            donestatusKeySwitcher = {
                1: 'futbadno1',
                0: 'futbadno0',
                -1: 'futbadno-1'
            }
            donestatusAnswSwitcher = {
                1: "Normalerweise freust du dich darauf, heute auch?",
                0: "Freust du dich heute?",
                -1: "Du freust dich normal nicht darauf, heute bestimmt auch nicht?"
            }

            session.attributes['session_key'] = donestatusKeySwitcher.get(donestatus, 'badmood')
            answ = donestatusAnswSwitcher.get(donestatus, "Das ist schade. Was machst du sonst so?")
        return question(answ)
    else:
        futurestatus = db.getFutureStatus(session.attributes['userID'], action)
        if (futurestatus != None):
            futurestatusKeySwitcher = {
                1: 'futgood1',
                0: 'futgood0',
                -1: 'futgood-1'
            }
            futurestatusAnswSwitcher = {
                1: "Du freust dich darauf, oder?",
                0: "Freust du dich jetzt?",
                -1: "Du freust dich nicht darauf, oder?"
            }

            session.attributes['session_key'] = futurestatusKeySwitcher.get(futurestatus, 'futgoodnono')
            answ = futurestatusAnswSwitcher.get(futurestatus, "Freust du dich?")
        else:
            donestatus = db.getDoneStatus(session.attributes['userID'], action)
            donestatusKeySwitcher = {
                1: 'futgoodno1',
                0: 'futgoodno0',
                -1: 'futgoodno-1'
            }
            donestatusAnswSwitcher = {
                1: "Normalerweise freust du dich darauf, heute auch?",
                0: "Freust du dich heute darauf?",
                -1: "Du freust dich normal nicht darauf, freust du dich heute?"
            }

            session.attributes['session_key'] = donestatusKeySwitcher.get(donestatus, 'futgoodnono')
            answ = donestatusAnswSwitcher.get(donestatus, "Freust du dich?")
        return question(answ)

#Vorschlaege fuer weitere Aktivitaeten
@ask.intent('SuggestionIntent')
def suggestion():
    print("SuggestionIntent")
    global counter 
    act = db.getActivity(session.attributes['userID'], counter)
    if act != None:
        counter += 1
        session.attributes['count'] = counter
        if db.getActivity(session.attributes['userID'], counter) != None:
            session.attributes['session_key'] = 'furthersuggestion'
            return question("Wie waere es mit {} . Soll ich dir eine weitere Aktivitaet vorschlagen, dann sag bitte Vorschlag oder Ende zum Beenden".format(act))
        else:
            return statement("Du koenntest {}".format(act))
    else:
        return statement("Leider kann ich dir noch keine Aktivitaet vorschlagen")

#geplante Aktivitaeten sagen
@ask.intent('TellFutureIntent')
def tell():
    print("TellFutureIntent")
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



if __name__ == '__main__':
    app.run(debug=True)