#!/usr/bin/env python

from flask import Flask, render_template
from flask_ask import Ask, statement, question
import mysql.connector

app = Flask(__name__)
ask = Ask(app, '/')

#Klasse Datenbank
class Datenbank:

    def __init__(self):
        '''
        Initializer calling connectDatenbank()
        :raise: mysql.connector.errors.Error
        '''
        try:
            Datenbank.__mydb = self.__connectDatenbank()
        except mysql.connector.errors.Error as e:
            raise

    #Verbindung auf- und abbauen
    def __connectDatenbank(self):
        '''
        Verbindung aufbauen
        :return: mysql.connector
        :raise: mysql.connector.errors.Error
        '''
        try:
            return mysql.connector.connect(host="localhost", user="Alexa", passwd="axelA", database="alexasmalltalkemotion")
        except mysql.connector.errors.Error as e:
            raise
    def disconnectDatenbank(self):
        '''
        Verbindung abbauen
        '''
        self.__mydb.close()
#Klasse Datenbank


#Beispiel-Code
try:
    db = Datenbank()
    print("db connected")
except mysql.connector.errors.Error as e:
    exit(str(e))

db.disconnectDatenbank()
print("db closed")
#Beispiel-Code


if __name__ == '__main__':
    app.run(debug=True)