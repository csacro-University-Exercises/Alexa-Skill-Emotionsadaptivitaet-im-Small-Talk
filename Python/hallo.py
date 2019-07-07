#!/usr/bin/env python

from flask import Flask, request
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
        session.attributes['userKnown'] = False
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
    if(session.attributes['userKnown']):
        return question("Ich habe die Eingabe nicht verstanden. Kannst du sie bitte anders formulieren?")
    session.attributes['session_key'] = 'how'
    userId = db.getUser(name)
    if userId == None:
        session.attributes['userID'] = db.createUser(name)
        session.attributes['userKnown'] = True
        session.attributes['session_key'] = 'how'
        return question("Hallo {}, freut mich dich kennen zu lernen. Zu Beginn eine kurze Einfuehrung. Du kannst mir nun Aktivitaeten nennen, die du entweder schon getan hast oder die fuer heute noch geplant sind. Sage dafuer zum Beispiel Ich werde zeichnen oder ich habe gezeichnet. Ausserdem kannst du dir mit dem Befehl Vorschlag eine Aktivitaet vorschlagen lassen oder mit Was nach deinen geplanten Aktivitaeten fragen. Beendet wird die Anwendung mit Ende. Aber nun, wie geht es dir denn heute?".format(name))
    else:
        session.attributes['userID'] = userId
        session.attributes['userKnown'] = True
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
        'how': 1,
        'badhow': -1,
        'shutdown': -1,
        'maybetalkin': 0
    }
    sessionKeyFuturestatusSwitcher = {
        'futgoodnono': 1,
        'futgoodno-1': 1,
        'futgoodno0': 1,
        'futgoodno1': 1,
        'futgood1': 1,
        'futgood0': 1,
        'futgood-1': 1,
        'futbad1': 1,
        'futbad0': -1,
        'futbad-1': 1,
        'futbadnono': 1,
        'futbadno1': 1,
        'futbadno0': 1,
        'futbadno-1': 1
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
        'futgoodno-1': "Schoen, dass du dich heute freust. Was machst du heute sonst so?",
        'futgoodno0': "Das freut mich. Was machst du heute sonst so?",
        'futgoodno1': "Das freut mich. Was machst du heute sonst so?",
        'futgood1': "Gut, dass du dich freust. Was machst du heute sonst so?",
        'futgood0': "Okay, was machst du heute sonst so?",
        'futgood-1': "Schoen, dass du deine Meinung geaendert hast. Was machst du heute sonst so?",
        'futbad1': "Gut, was machst du heute sonst so?",
        'futbad0': "Okay, was machst du heute sonst so?",
        'futbad-1': "Oh das ist schoen. Was machst du heute sonst so?",
        'futbadnono': "Okay, was machst du heute sonst so?",
        'futbadno1': "Gut, dass deine Laune nicht deine Freude truebt. Was machst du heute sonst so?",
        'futbadno0': "Okay, was machst du heute sonst so?",
        'futbadno-1': "Okay das freut mich. Was machst du heute sonst so?",
        'pastgoodnono': "Okay, was machst du heute sonst so?",
        'pastgoodno1': "Super. Was hast du sonst so vor oder hast du gemacht?",
        'pastgoodno0': "Das ist toll. Erzaehl mir von deinen anderen Aktivitaeten.",
        'pastgoodno-1': "Schoen, dass du doch Spass hattest. Was ist heute sonst so gewesen?",
        'pastgood1': "Super, dass es gut war. Was machst du heute sonst so schoenes?",
        'pastgood0': "Okay, wenigstens war es nicht schlecht. Was machst du heute sonst so?",
        'pastgood-1': "Das ist nicht gut. Was fuer Aktivitaeten machst du heute sonst so?",
        'pastbadnono': "Okay, was machst du heute sonst so?",
        'pastbadno1': "Gut dass es dir trotzdem Spass macht. Was machst du heute sonst so?",
        'pastbadno0': "Ah das ist schoen. Erzaehl mir was du sonst so machst oder gemacht hast.",
        'pastbadno-1': "Okay, dann weiss ich Bescheid. Gibt es sonst etwas das dir den Tag verdorben hat?",
        'pastbad1': "Schade, dass dich deine Laune beeinflusst hat. Gibt es sonst noch etwas?",
        'pastbad0': "Wenigstens war es nicht schlecht. Was machst du heute sonst so?",
        'pastbad-1': "Das ist sehr schade, aber war zu erwarten. Machst du sonst etwas schoenes oder hast etwas gemacht?"
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
        print("db disconnected")
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
        'futgoodno-1': "Wenigstens findest du es okay. Machst du heute sonst noch etwas oder hast etwas gemacht?",
        'futgoodno0': "Okay, was machst du heute sonst so?",
        'futgoodno1': "Okay, man kann sich ja nicht immer freuen. Was machst du heute sonst so?",
        'futgood1': "Okay, was machst du heute sonst so?",
        'futgood0': "Okay, was machst du heute sonst so?",
        'futgood-1': "Okay, was machst du heute sonst so?",
        'futbad1': "Okay, was machst du heute sonst so?",
        'futbad0': "Okay, was machst du heute sonst so?",
        'futbad-1': "Das dachte ich mir schon. Was machst du heute sonst so?",
        'futbadnono': "Okay, was machst du heute sonst so?",
        'futbadno1': "Okay, was machst du heute sonst so?",
        'futbadno0': "Okay, was machst du heute sonst so?",
        'futbadno-1': "Okay, was machst du heute sonst so?",
        'pastgoodnono': "Okay, was machst du heute sonst so?",
        'pastgoodno1': "Okay, alles klar. Was machst du heute sonst so?",
        'pastgoodno0': "Okay, na gut. Was machst du heute sonst so?",
        'pastgoodno-1': "Okay, was machst du heute sonst so?",
        'pastgood1': "Okay, na gut. Was machst du heute sonst so?",
        'pastgood0': "Okay, was machst du heute sonst so?",
        'pastgood-1': "Wenigstens war es ein bisschen besser als erwartet. Was machst du heute sonst so?",
        'pastbadnono': "Okay, was machst du heute sonst so?",
        'pastbadno1': "Okay, was machst du heute sonst so?",
        'pastbadno0': "Okay, was machst du heute sonst so?",
        'pastbadno-1': "Also nur ein bisschen. Was machst du heute sonst so?",
        'pastbad1': "Okay, was machst du heute sonst so?",
        'pastbad0': "Okay, was machst du heute sonst so?",
        'pastbad-1': "Wenigstens war es so la la. Was machst du heute sonst so?"
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
        'futbad1': -1,
        'futbad0': 1,
        'futbad-1': -1,
        'futbadnono': -1,
        'futbadno1': -1,
        'futbadno0': -1,
        'futbadno-1': -1
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
        'futgoodnono': "Schade, dass du dich nicht freust. Was machst du heute sonst noch?",
        'futgoodno-1': "Okay, was machst du heute sonst noch?",
        'futgoodno0': "Das ist schade. Was machst du heute sonst noch?",
        'futgoodno1': "Schade, dass du dich diesmal nicht freust. Gibt es sonst etwas, dass du heute noch machst oder gemacht hast?",
        'futgood1': "Schade, dass du dich nicht mehr freust. Was machst du heute sonst noch?",
        'futgood0': "Okay, was machst du heute sonst noch?",
        'futgood-1': "Schade, dass du dich immer noch nicht freust. Was machst du heute sonst noch?",
        'futbad1': "Das tut mir leid. Was machst du heute sonst noch?",
        'futbad0': "Schade, aber was machst du heute sonst noch?",
        'futbad-1': "Okay, was machst du heute sonst noch?",
        'futbadnono': "Okay, was machst du heute sonst noch?",
        'futbadno1': "Das liegt bestimmt an deiner Laune, aber was machst du denn sonst noch?",
        'futbadno0': "Okay, was machst du heute sonst noch?",
        'futbadno-1': "Das dachte ich mir. Gibt es sonst noch etwas das du getan hast oder tun wirst?",
        'pastgoodnono': "Okay, was machst du heute sonst noch?",
        'pastgoodno1': "Oh das ist sehr schade. Moechtest du mir sonst von einer Aktivitaet erzaehlen?",
        'pastgoodno0': "Schade, dass du keinen Spass hattest. Was machst du heute sonst noch?",
        'pastgoodno-1': "Schade, das dachte ich mir. Erzaehl mir doch was du sonst so machst?",
        'pastgood1': "Das ist sehr schade. Was hast du sonst gemacht oder wirst du machen?",
        'pastgood0': "Schade, dass es schlechter war. Erzaehl mir doch was du sonst so machst.",
        'pastgood-1': "Ah freut mich, dass es besser war. Was machst du heute sonst noch?",
        'pastbadnono': "Okay, was machst du heute sonst noch?",
        'pastbadno1': "Schade, was hast du denn sonst geplant?",
        'pastbadno0': "Oh das ist schade. Was ist denn sonst so geplant?",
        'pastbadno-1': "Okay alles klar. Gibt es sonst noch etwas?",
        'pastbad1': "Schoen, dass es trotzdem Spass gemacht hat. Was gibt es sonst so?",
        'pastbad0': "Oh das tut mir leid. Was hast du sonst so gemacht oder hast du vor?",
        'pastbad-1': "Freut mich, dass es doch besser war. Erzaehl mir doch was du sonst so machst"
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
        print("db disconnected")
        return statement(answ)
    else:
        return question(answ)

@ask.intent('PastActivityIntent')
def action():
    print("PastActivityIntent")
    content = request.get_json()
    session.attributes['action'] = (content['request']['intent']['slots']['action']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name'])
    action = session.attributes['action']

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

@ask.intent('FutureActivityIntent')
def action():
    print("FutureActivityIntent")
    content = request.get_json()
    session.attributes['action'] = (content['request']['intent']['slots']['action']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name'])
    action = session.attributes['action']
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
                1: "Normalerweise freust du dich darauf, heute auch, obwohl du schlecht gelaunt bist?",
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
            return question("Du koenntest {} . Fuer einen weiteren Vorschlag, sag bitte Vorschlag. Zum Beenden, sag Ende.".format(act))
        else:
            db.disconnectDatenbank()
            print("db disconnected")
            return statement("Du koenntest {}. Da ich keine weiteren Vorschlaege habe, werde ich mich beenden".format(act))
    else:
        db.disconnectDatenbank()
        print("db disconnected")
        return statement("Leider kann ich dir noch keine Aktivitaet vorschlagen. Bis zum naechsten Mal.")

#geplante Aktivitaeten sagen
@ask.intent('TellFutureIntent')
def tell():
    print("TellFutureIntent")
    activities = db.getFutureActivities(session.attributes['userID'])
    if activities == None:
        return question("Ich kenne deine Plaene fuer heute nicht. Erzaehle mir bitte, was du vor hast.")
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
        liste += " geplant. Was hast du heute sonst noch vor?"
        return question(liste)

@ask.intent('AMAZON.FallbackIntent')
def fall():
    return question("Ich habe die Eingabe nicht verstanden. Kannst du sie bitte wiederholen?")

@ask.intent('AMAZON.HelpIntent')
def help():
    return question("Du befindest dich im Smalltalk-Skill. Du kannst mir nun Aktivitaeten nennen, die du entweder schon getan hast oder die fuer heute noch geplant sind. Sage dafuer zum Beispiel Ich werde zeichnen oder ich habe gezeichnet. Ausserdem kannst du dir mit dem Befehl Vorschlag eine Aktivitaet vorschlagen lassen oder mit Was nach deinen geplanten Aktivitaeten fragen. Beendet wird die Anwendung mit Ende.")

if __name__ == '__main__':
    app.run(debug=True)
