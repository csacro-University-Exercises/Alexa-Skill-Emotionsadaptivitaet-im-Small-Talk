#!/usr/bin/env python

from __future__ import division
from flask import Flask, render_template
from flask_ask import Ask, statement, question
import mysql.connector

app = Flask(__name__)
ask = Ask(app, '/')

#Klasse Datenbank
class Datenbank:

    def __init__(self):
        """
        Initializer calling connectDatenbank()
        :raise: mysql.connector.errors.Error
        """
        try:
            Datenbank.__mydb = self.__connectDatenbank()
        except mysql.connector.errors.Error as e:
            raise

    #Hilfsmethode: AutoIncrement reset
    def __resetAutoIncrement(self, table):
        try:
            cursor = self.__mydb.cursor()
            query = "ALTER TABLE %s AUTO_INCREMENT = 1"
            query_param = (table,)
            cursor.execute(query, query_param)
            cursor.close()
        except mysql.connector.errors.Error as e:
            print(str(e))

    #Hilsmethoden: ActivityId
    def __activityId(self, activity):
        try:
            id = self.__getActivityId(activity)
            if (id == None):
                id = self.__createActivity(activity)
            return id
        except mysql.connector.errors.Error as e:
            raise
    def __getActivityId(self, activity):
        try:
            cursor = self.__mydb.cursor()
            query = "SELECT ActivityId FROM activity WHERE ActivityName = %s"
            query_param = (activity,)
            cursor.execute(query, query_param)
            result = cursor.fetchone()
            cursor.close()
            if (result != None):
                result = result[0]
            return result
        except mysql.connector.errors.Error as e:
            raise
    def __createActivity(self, activity):
        try:
            cursor = self.__mydb.cursor()
            query = "INSERT INTO activity (ActivityName) VALUES (%s)"
            query_param = (activity,)
            cursor.execute(query, query_param)
            self.__mydb.commit()
            cursor.close()
            return self.__getActivityId(activity)
        except mysql.connector.errors.Error as e:
            self.__mydb.rollback()
            self.__resetAutoIncrement("activity")
            raise

    #Hilfsmehtode: round status
    def __round(self, num):
        if (num < -0.33):
            roundednum = -1
        elif (num > 0.33):
            roundednum = 1
        else:
            roundednum = 0
        return roundednum

    #Hilfsmethoden: FutureActivityStatus
    def __createFutureAcitivtyStatus(self, userId, activity, status):
        try:
            cursor = self.__mydb.cursor()
            query = "INSERT INTO futureactivities (UserId, ActivityId, Status) VALUES (%s, %s, %s)"
            query_param = (userId, self.__activityId(activity), status)
            cursor.execute(query, query_param)
            self.__mydb.commit()
            cursor.close()
        except mysql.connector.errors.Error as e:
            self.__mydb.rollback()
            raise
    def __updateFutureActivityStatus(self, userId, activity, status):
        try:
            cursor = self.__mydb.cursor()
            query = "UPDATE futureactivities SET Status = %s WHERE UserId = %s AND ActivityId = %s"
            query_param = (status, userId, self.__activityId(activity))
            cursor.execute(query, query_param)
            self.__mydb.commit()
            cursor.close()
        except mysql.connector.errors.Error as e:
            self.__mydb.rollback()
            raise

    #Hilfmethoden: DoneActivityStatus
    def __createDoneAcitivtyStatus(self, userId, activity, status):
        try:
            cursor = self.__mydb.cursor()
            query = "INSERT INTO doneactivities (UserId, ActivityId, Status) VALUES (%s, %s, %s)"
            query_param = (userId, self.__activityId(activity), status)
            cursor.execute(query, query_param)
            self.__mydb.commit()
            cursor.close()
        except mysql.connector.errors.Error as e:
            self.__mydb.rollback()
            raise
    def __updateDoneActivityStatus(self, userId, activity, status):
        try:
            cursor = self.__mydb.cursor()
            query = "UPDATE doneactivities SET Status = Status + %s, Count = Count + 1 WHERE UserId = %s AND ActivityId = %s"
            query_param = (status, userId, self.__activityId(activity))
            cursor.execute(query, query_param)
            self.__mydb.commit()
            cursor.close()
        except mysql.connector.errors.Error as e:
            self.__mydb.rollback()
            raise

    #Verbindung auf- und abbauen
    def __connectDatenbank(self):
        """
        Verbindung aufbauen
        :return: mysql.connector
        :raise: mysql.connector.errors.Error
        """
        try:
            datenbank = mysql.connector.connect(host="localhost", user="Alexa", passwd="axelA", database="alexasmalltalkemotion")
            try:
                cursor = datenbank.cursor()
                query = "DELETE FROM futureactivities WHERE CONVERT(lastStatusDate, DATE) != CURRENT_DATE"
                cursor.execute(query)
                datenbank.commit()
                cursor.close()
            except mysql.connector.errors.Error as e:
                datenbank.rollback()
                raise
            return datenbank
        except mysql.connector.errors.Error as e:
            raise
    def disconnectDatenbank(self):
        """
        Verbindung abbauen
        """
        self.__mydb.close()

    #User abfragen und ggf. anlegen
    def getUser(self, userName):
        """
        User abfragen
        :param userName: erhalten durch Alexa
        :return UserId: UserName gefunden
                None: UserName nicht gefunden
        :raise: mysql.connector.errors.Error
        """
        try:
            cursor = self.__mydb.cursor()
            query = "SELECT UserId FROM user WHERE UserName = %s"
            query_param = (userName,)
            cursor.execute(query, query_param)
            result = cursor.fetchone()
            cursor.close()
            if(result != None):
                result = result[0]
            return result
        except mysql.connector.errors.Error as e:
            raise
    def createUser(self, userName):
        """
        User anlegen
        :param userName: erhalten durch Alexa
        :return: UserId
        :raise: mysql.connector.errors.Error
        """
        try:
            cursor = self.__mydb.cursor()
            query = "INSERT INTO user (UserName) VALUES (%s)"
            query_param = (userName,)
            cursor.execute(query, query_param)
            self.__mydb.commit()
            cursor.close()
            return self.getUser(userName)
        except mysql.connector.errors.Error as e:
            self.__mydb.rollback()
            self.__resetAutoIncrement("user")
            raise

    #User Feeling-Feld lesen und schreiben
    def getUserFeeling(self, userId):
        """
        User Feeling-Feld lesen
        :param userId: erhalten durch getUser-Methode bzw. createUser-Methode
        :return 1: gruen
                0: gelb
                -1: rot
                None: Feeling-Feld leer oder lastFeelingDate nicht heute
        :raise: mysql.connector.errors.Error
        """
        try:
            cursor = self.__mydb.cursor()
            query = "SELECT Feeling FROM user WHERE UserId = %s AND CONVERT(lastFeelingDate, DATE) = CURRENT_DATE"
            query_param = (userId,)
            cursor.execute(query, query_param)
            result = cursor.fetchone()
            cursor.close()
            if(result != None):
                result = result[0]
            return result
        except mysql.connector.errors.Error as e:
            raise
    def setUserFeeling(self, userId, feeling):
        """
        User Feeling-Feld schreiben
        :param userId: erhalten durch getUser-Methode bzw. createUser-Methode
        :param feeling: gruen --> 1
                        gelb --> 0
                        rot --> -1
        :raise: mysql.connector.errors.Error
        """
        try:
            cursor = self.__mydb.cursor()
            query = "UPDATE user SET Feeling = %s WHERE UserId = %s"
            query_param = (feeling, userId)
            cursor.execute(query, query_param)
            self.__mydb.commit()
            cursor.close()
        except mysql.connector.errors.Error as e:
            self.__mydb.rollback()
            raise

    #Activities Status-Feld lesen
    def getFutureStatus(self, userId, activity):
        """
        FutureActivities Status-Feld lesen
        :param userId: erhalten durch getUser-Methode bzw. createUser-Methode
        :param activity: erhalten durch Alexa-Abfrage
        :return 1: gruen
                0: gelb
                -1: rot
                None: Status-Feld leer oder lastStatusDate nicht heute
        :raise: mysql.connector.errors.Error
        """
        try:
            cursor = self.__mydb.cursor()
            query = "SELECT Status FROM futureactivities WHERE UserId = %s AND ActivityId = %s"
            query_param = (userId, self.__activityId(activity))
            cursor.execute(query, query_param)
            result = cursor.fetchone()
            cursor.close()
            if(result != None):
                result = result[0]
            return result
        except mysql.connector.errors.Error as e:
            raise
    def getDoneStatus(self, userId, activity):
        """
        DoneActivities Status-Feld lesen
        :param userId: erhalten durch getUser-Methode bzw. createUser-Methode
        :param activity: erhalten durch Alexa-Abfrage
        :return 1: gruen
                0: gelb
                -1: rot
                None: Status-Feld leer
        :raise: mysql.connector.errors.Error
        """
        try:
            cursor = self.__mydb.cursor()
            query = "SELECT Status, Count FROM doneactivities WHERE UserId = %s AND ActivityId = %s"
            query_param = (userId, self.__activityId(activity))
            cursor.execute(query, query_param)
            result = cursor.fetchone()
            cursor.close()
            if(result != None):
                result = self.__round(result[0]/result[1])
            return result
        except mysql.connector.errors.Error as e:
            raise

    #Activities Status-Feld schreiben
    def setFutureStatus(self, userId, activity, status):
        """
        FutureActivities Status-Feld schreiben
        :param userId: erhalten durch getUser-Methode bzw. createUser-Methode
        :param activity: erhalten durch Alexa-Abfrage
        :param status: gruen --> 1
                        gelb --> 0
                        rot --> -1
        :raise: mysql.connector.errors.Error
        """
        try:
            if(self.getFutureStatus(userId, activity) == None):
                self.__createFutureAcitivtyStatus(userId, activity, status)
            else:
                self.__updateFutureActivityStatus(userId, activity, status)
        except mysql.connector.errors.Error as e:
            raise
    def setDoneStatus(self, userId, activity, status):
        """
        FutureActivities Status-Feld schreiben
        :param userId: erhalten durch getUser-Methode bzw. createUser-Methode
        :param activity: erhalten durch Alexa-Abfrage
        :param status: gruen --> 1
                        gelb --> 0
                        rot --> -1
        :raise: mysql.connector.errors.Error
        """
        try:
            if (self.getDoneStatus(userId, activity) == None):
                self.__createDoneAcitivtyStatus(userId, activity, status)
            else:
                self.__updateDoneActivityStatus(userId, activity, status)
        except mysql.connector.errors.Error as e:
            raise

    #Aktivitaet vorschlagen
    def getActivity(self, userId, tries):
        """
        schlaegt eine Aktivitaet vor
        :param UserId: erhalten durch getUser-Methode bzw. createUser-Methode
        :param tries: Anzahl der Versuche Aktiviteatsvorschlag zu geben
        :return Activitaet: Name der vorgeschlagenen Aktivitaet
                None: User hat keine tries-viele Aktivitaeten in doneactivities eingetragen, die nicht fuer heute geplant sind und "gruen" oder "gelb" sind
        :raise: mysql.connector.errors.Error
        """
        try:
            cursor = self.__mydb.cursor()
            query = "SELECT ActivityName FROM activity JOIN doneactivities ON activity.ActivityId = doneactivities.ActivityId WHERE UserId = %s AND Status/Count >= -0.33 AND doneactivities.ActivityId NOT IN (SELECT ActivityId FROM futureactivities WHERE UserId = %s) ORDER BY Status/Count DESC, CONVERT(lastStatusDate, DATE) != CURRENT_DATE ASC LIMIT 1 OFFSET %s"
            query_param = (userId, userId, tries-1)
            cursor.execute(query, query_param)
            result = cursor.fetchone()
            cursor.close()
            if(result != None):
                result = result[0]
            return result
        except mysql.connector.errors.Error as e:
            raise

    #FutureActivities auslesen
    def getFutureActivities(self, userId):
        """
        FutureActivities auslesen
        :param UserId: erhalten durch getUser-Methode bzw. createUser-Methode
        :return Activitaeten: Array mit Namen der Aktivitaeten
                None: User hat keine Aktivitaeten in futureactivities eingetragen, die heute sind
        :raise: mysql.connector.errors.Error
        """
        try:
            cursor = self.__mydb.cursor()
            query = "SELECT ActivityName FROM activity JOIN futureactivities ON activity.ActivityId = futureactivities.ActivityId WHERE UserId = %s ORDER BY CONVERT(lastStatusDate, DATE) != CURRENT_DATE ASC"
            query_param = (userId,)
            cursor.execute(query, query_param)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.errors.Error as e:
            raise
    #FutureActivity loeschen oder in doneactivities mit Status umschreiben
    def deleteFutureActivity(self, userId, activity):
        """
        FutureActivity loeschen
        :param UserId: erhalten durch getUser-Methode bzw. createUser-Methode
        :param activity: erhalten durch Alexa-Abfrage
        :raise: mysql.connector.errors.Error
        """
        try:
            cursor = self.__mydb.cursor()
            query = "DELETE FROM futureactivities WHERE UserId = %s AND ActivityId = %s"
            query_param = (userId, self.__activityId(activity))
            cursor.execute(query, query_param)
            self.__mydb.commit()
            cursor.close()
        except mysql.connector.errors.Error as e:
            self.__mydb.rollback()
            raise
    def moveFutureActivityToDone(self, userId, activity, status):
        """
        FutureActivity in doneactivities mit Status umschreiben
        :param UserId: erhalten durch getUser-Methode bzw. createUser-Methode
        :param activity: erhalten durch Alexa-Abfrage
        :param status: gruen --> 1
                        gelb --> 0
                        rot --> -1
        :raise: mysql.connector.errors.Error
        """
        try:
            self.deleteFutureActivity(userId, activity)
            self.setFutureStatus(userId, activity, status)
        except mysql.connector.errors.Error as e:
            raise

#Klasse Datenbank


#Beispiel-Code
user = "Carolin"
feel = 0
act = "asdf"
futstat = 0
donestat = 1

try:
    db = Datenbank()
    print("db connected")
except mysql.connector.errors.Error as e:
    exit(str(e))

try:
    id = db.getUser(user)
    print("getUser: %s" % id)
except mysql.connector.errors.Error as e:
    exit(str(e))

if(id == None):
    try:
        id = db.createUser(user)
        print("createUser: %s" % id)
    except mysql.connector.errors.Error as e:
        exit(str(e))

try:
    feeling = db.getUserFeeling(id)
    print("getFeeling: %s" % feeling)
except mysql.connector.errors.Error as e:
    exit(str(e))

try:
    db.setUserFeeling(id, feel)
    print("setFeeling")
except mysql.connector.errors.Error as e:
    exit(str(e))

try:
    futureStatus = db.getFutureStatus(id, act)
    print("getFutureStatus: %s" % futureStatus)
except mysql.connector.errors.Error as e:
    exit(str(e))

try:
    doneStatus = db.getDoneStatus(id, act)
    print("getDoneStatus: %s" % doneStatus)
except mysql.connector.errors.Error as e:
    exit(str(e))

try:
    db.setFutureStatus(id, act, futstat)
    print("setFutureStatus")
except mysql.connector.errors.Error as e:
    exit(str(e))

try:
    db.setDoneStatus(id, act, donestat)
    print("setDoneStatus")
except mysql.connector.errors.Error as e:
    exit(str(e))

try:
    for i in range(1, 5):
        vorschlag = db.getActivity(id, i)
        print("getActivity, Vorschlag %s: %s" % (i, vorschlag))
except mysql.connector.errors.Error as e:
    exit(str(e))

try:
    futureact = db.getFutureActivities(id)
    for i in range(0, len(futureact)):
        print("getFutureActivities %s: %s" % (i, futureact[i][0]))
except mysql.connector.errors.Error as e:
    exit(str(e))

#try:
#    db.deleteFutureActivity(id, act)
#    print("deleteFutureActivity")
#except mysql.connector.errors.Error as e:
#    exit(str(e))

#try:
#    db.moveFutureActivityToDone(id, act, 1)
#    print("moveFutureActivityToDone")
#except mysql.connector.errors.Error as e:
#    exit(str(e))

db.disconnectDatenbank()
print("db closed")
#Beispiel-Code


if __name__ == '__main__':
    app.run(debug=True)