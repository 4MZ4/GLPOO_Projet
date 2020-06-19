# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime

def Convert_Data( data):
        output = []
        for i in data:
            output.append( i[1] )
        return output 
def Correction_Date( date):
        date_split = date.split('-')
        if( len( date_split[1] ) == 1 ) : 
            date_split[1] = "0"+date_split[1]
        if( len( date_split[2] ) == 1 ) : 
            date_split[2] = "0"+date_split[2]
        date = date_split[0]+"-"+date_split[1]+"-"+date_split[2]
        return date
def Validation_Date(  date ):
        date_split = date.split('-')
        if len(date_split) != 3  :
            return 0
        try:
            if datetime(int(date_split[0] ),int(date_split[1] ),int(date_split[2] ) ) :
                return 1
        except:
            return 0
        
class DATABASE:
    def __init__(self):
        self.connection = sqlite3.connect('DATABASE.db')
        self.cursor = self.connection.cursor()
    def GET_severity(self):
        self.cursor.execute("SELECT * FROM severity ;")
        return self.cursor.fetchall()
    def GET_timezone(self):
        self.cursor.execute("SELECT * FROM timezone ;")
        return self.cursor.fetchall()
    def GET_type(self):
        self.cursor.execute("SELECT * FROM type ;")
        return self.cursor.fetchall()
    def GET_airport(self):
        self.cursor.execute("SELECT * FROM airport ;")
        return self.cursor.fetchall()
    def GET_new_index_event(self):
        self.cursor.execute("SELECT COUNT(EventID) from Event_;")
        return self.cursor.fetchall()[0][0]+1
    def Delete_by_index(self , ID ):
        query = """ DELETE FROM event_
                where EventID = """+str(ID)+" ;"
        self.cursor.execute(query)
        self.connection.commit()
    def GET_data_by_ID(self, ID ):
        query = """ SELECT DATE(StartTime) , DATE(EndTime) , TimeZone , Severity , Type , AirportCode ,  ev.SeverityID , ev.TypeID , ev.TimeZoneID , ev.AirportID  FROM event_ as ev
                JOIN severity as sev on sev.SeverityID = ev.SeverityID
                JOIN type as ty on ty.TypeID = ev.TypeID
                JOIN timezone as tz on tz.TimeZoneID = ev.TimeZoneID
                JOIN airport as air on air.AirportID = ev.AirportID
                where EventID = """+str(ID)+" ;"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def GET_principale(self):
        query = """SELECT EventID , DATE( StartTime ) , DATE( EndTime ) , Severity , TimeZone , Type , AirportCode , City , County , State  FROM event_ as ev
                JOIN severity as sev on sev.SeverityID = ev.SeverityID
                JOIN timezone as tz on tz.TimeZoneID = ev.TimeZoneID
                JOIN type as ty on ty.TypeID = ev.TypeID
                JOIN airport as air on air.AirportID = ev.AirportID
                JOIN city as ct on ct.CityID = air.CityID
                JOIN county as cn on cn.CountyID = ct.CountyID
                JOIN state as st on st.StateID = cn.StateID
                order by  EventID DESC
                limit 30;"""
        self.cursor.execute(query)
        return self.cursor.fetchall()
    def Run_Query(self , query):
        self.cursor.execute( query )
        self.connection.commit()
    def Close(self):
        self.cursor.close()
        self.connection.close()

        