# -*- coding: utf-8 -*-
import sqlite3 , numpy , pandas

data = pandas.read_csv("US_WeatherEvents_2016-2019.csv")
data = data.apply(lambda x: x.fillna(-1) if x.dtype.kind in 'biufc' else x.fillna('.')) ##NaN can't be put in mysql dataframe

# fonction fait une indexation
def Indexation(table, index_table):
    index = {}
    cnt = 0  # creation d'un dictionnaire vide index , et conteur à 0
    for i in table[index_table]:  # on parcour notre colonne index_table de la table
        if i not in index:
            index[i] = cnt
            cnt += 1  # si l'index n'est pas dans le dictionnaire en le crée sinon on saute
    table[index_table] = table[index_table].replace(index)
    # cette fonction nous permet de ramplacer les valeur de la colonne index_table grace au dictionnaire index
    return pandas.DataFrame(numpy.array(list(index.items())), columns=[index_table, index_table + "ID"])
    # retourne la table d'index sous forme de Dataframe_pandas avec des colonnes nommées

# =============================================================================
# Timezone indexation
# type indexation
# severity indexation
# state indexation

index_timezone = Indexation(data, 'TimeZone')
index_timezone = index_timezone.reindex(columns=['TimeZoneID', 'TimeZone'])
data.rename(columns={'TimeZone': 'TimeZoneID'}, inplace=True)

index_type = Indexation(data, 'Type')
index_type = index_type.reindex(columns=['TypeID', 'Type'])
data.rename(columns={'Type': 'TypeID'}, inplace=True)

index_severity = Indexation(data, 'Severity')
index_severity = index_severity.reindex(columns=['SeverityID', 'Severity'])
data.rename(columns={'Severity': 'SeverityID'}, inplace=True)

index_State = Indexation(data, 'State')
index_State = index_State.reindex(columns=['StateID', 'State'])
data.rename(columns={'State': 'StateID'}, inplace=True)

# =============================================================================
# Airportcode indexation
position_lat_long_airport = {}

for i in data[['AirportCode', 'LocationLat', 'LocationLng', 'StateID']].values:
    if i[0] not in position_lat_long_airport:
        position_lat_long_airport[i[0]] = [i[1], i[2], i[3]]
        # print(position_lat_long_airport[i[0]])

index_Airport = Indexation(data, 'AirportCode')
airport = []

for i in index_Airport.values:
    e = position_lat_long_airport[i[0]]  # e for element
    airport.append([i[0], i[1], e[0], e[1], e[2]])

data.rename(columns={'AirportCode': 'AirportCodeID'}, inplace=True)
data[['AirportCodeID', 'LocationLat', 'LocationLng', 'StateID']] = data[
    ['AirportCodeID', 'LocationLat', 'LocationLng', 'StateID']].replace(airport[1:])
index_Airport = pandas.DataFrame(airport,
                                 columns=['AirportCode', 'AirportCodeID', 'LocationLat', 'LocationLng', 'StateID'])
index_Airport = index_Airport.reindex(columns=['AirportCodeID', 'AirportCode', 'LocationLat', 'LocationLng', 'StateID'])
# =============================================================================
# Country indexation
index_County = Indexation(data, 'County')
data.rename(columns={'County': 'CountyID'}, inplace=True)
data.CountyID = data.CountyID.astype(int)

index_County.CountyID = index_County.CountyID.astype(int)
index_County = index_County.merge(data[['CountyID', 'ZipCode', 'StateID']], how='inner', on='CountyID')
index_County = index_County.sort_values('CountyID').drop_duplicates(['CountyID', 'StateID'], keep='last')
index_County = index_County.reindex(columns=['CountyID', 'County', 'ZipCode', 'StateID'])

# =============================================================================
# City indexation
index_City = Indexation(data, 'City')
data.rename(columns={'City': 'CityID'}, inplace=True)
data.CityID = data.CityID.astype(int)
index_City.CityID = index_City.CityID.astype(int)

index_City = index_City.merge(data[['CityID', 'CountyID']], how='inner', on='CityID')
index_City = index_City.sort_values('CityID').drop_duplicates(['CityID', 'CountyID'], keep='last')
index_City = index_City.reindex(columns=['CityID', 'City', 'CountyID'])

# =============================================================================
# Event table
event = data.drop(['LocationLat', 'LocationLng', 'ZipCode','CityID', 'CountyID', 'StateID'], axis=1)
event.insert(0, 'EventID', numpy.arange(0, len(event)))
event = event.reindex(columns=['EventID', 'StartTime(UTC)', 'EndTime(UTC)',
                                         'SeverityID', 'TypeID', 'TimeZoneID','AirportCodeID'])
del data


#==============================================================================
# Create tuples
event = list(event.to_records(index=False))
index_City = list(index_City.to_records(index=False))
index_County = list(index_County.to_records(index=False))
index_Airport = list(index_Airport.to_records(index=False))
index_State = list(index_State.to_records(index=False))
index_severity = list(index_severity.to_records(index=False))
index_type = list(index_type.to_records(index=False))
index_timezone = list(index_timezone.to_records(index=False))


try:    
    conn = sqlite3.connect('DATABASE.db')
    
    cursor = conn.cursor()
        
    try:
            query = ["""CREATE TABLE IF NOT EXISTS TimeZone(
           TimeZoneID INT,
           TimeZone VARCHAR(50),
           PRIMARY KEY(TimeZoneID)
           );""","""
        CREATE TABLE IF NOT EXISTS Type(
           TypeID INT,
           Type VARCHAR(50),
           PRIMARY KEY(TypeID)
        );""","""
        CREATE TABLE IF NOT EXISTS Severity(
           SeverityID INT,
           Severity VARCHAR(50),
           PRIMARY KEY(SeverityID)
        );
        ""","""
        CREATE TABLE IF NOT EXISTS State(
           StateID INT,
           State VARCHAR(50),
           PRIMARY KEY(StateID)
        );
        ""","""
        CREATE TABLE IF NOT EXISTS County(
           CountyID INT,
           County VARCHAR(254),
           ZipCode INT,
           StateID INT NOT NULL,
           PRIMARY KEY(CountyID),
           FOREIGN KEY(StateID) REFERENCES State(StateID)
        );
        ""","""
        CREATE TABLE IF NOT EXISTS City(
           CityID INT,
           City VARCHAR(50),
           CountyID INT NOT NULL,
           PRIMARY KEY(CityID),
           FOREIGN KEY(CountyID) REFERENCES County(CountyID)
        );""","""
        CREATE TABLE IF NOT EXISTS Airport(
           AirportID INT,
           AirportCode VARCHAR(50),
           LocationLat DOUBLE,
           LocationLng DOUBLE,
           CityID INT NOT NULL,
           PRIMARY KEY(AirportID),
           FOREIGN KEY(CityID) REFERENCES City(CityID)
        );""","""
        CREATE TABLE IF NOT EXISTS Event_(
           EventID INT,
           StartTime DATETIME,
           EndTime DATETIME,
           SeverityID INT NOT NULL,
           TypeID INT NOT NULL,
           TimeZoneID INT NOT NULL,
           AirportID INT NOT NULL,
           PRIMARY KEY(EventID),
           FOREIGN KEY(SeverityID) REFERENCES Severity(SeverityID),
           FOREIGN KEY(TypeID) REFERENCES Type(TypeID),
           FOREIGN KEY(TimeZoneID) REFERENCES TimeZone(TimeZoneID),
           FOREIGN KEY(AirportID) REFERENCES Airport(AirportID)
        );
            """]
            for q in query :
                cursor.execute(q )
            conn.commit()
    except conn.Error as err:
            print("Failed to create tables: {}".format(err))
            
 #=============================================================================        
    try:
            for e in index_timezone:
                query = "INSERT INTO TimeZone(TimeZoneID, TimeZone) VALUES ("+str(e[0])+", '"+str(e[1])+"');"
                cursor.execute(query)
            conn.commit()
            
            print("Inserting into TimeZone ==> 100%")
    except conn.Error as err:
            print("Failed to insert into table in SqLite: {}".format(err))
 #=============================================================================           
       
    try:
            for e in index_type:
                query = "INSERT INTO Type(TypeID, Type) VALUES ("+str(e[0])+", '"+str(e[1])+"');"
                cursor.execute(query)
            conn.commit()
            
            print("Inserting into Type ==> 100%")
    except conn.Error as err:
            print("Failed to insert into table in SqLite: {}".format(err))
 #=============================================================================               
            
    try:    
            for e in index_severity:
                query = "INSERT INTO Severity(SeverityID, Severity) VALUES ("+str(e[0])+", '"+str(e[1])+"');"
                cursor.execute(query)
            conn.commit()
            
            print("Inserting into Severity ==> 100%")
    except conn.Error as err:
            print("Failed to insert into table in SqLite: {}".format(err))
 #=============================================================================          
            
    try:    
            for e in index_State:
                query = "INSERT INTO State(StateID, State) VALUES ("+str(e[0])+", '"+str(e[1])+"');"
                cursor.execute(query)
            conn.commit()
            
            print("Inserting into State ==> 100%")
    except conn.Error as err:
            print("Failed to insert into table in SqLite: {}".format(err))
 #=============================================================================            
            
    try:
            for e in index_County:
                query = "INSERT INTO County(CountyID, County, ZipCode, StateID) VALUES ("+str(e[0])+", '"+str(e[1])+"', "+str(e[2])+", "+str(e[3])+");"
                cursor.execute(query)    
            conn.commit()
                    
            print("Inserting into Severity ==> 100%")
    except conn.Error as err:
            print("Failed to insert into table in SqLite: {}".format(err))
 #=============================================================================
    try:
            for e in index_City:
                query = "INSERT INTO City(CityID, City, CountyID) VALUES ("+str(e[0])+", '"+str(e[1])+"', "+str(e[2])+");"
                cursor.execute(query) 
            conn.commit()
                
            print("Inserting into City ==> 100%")
    except conn.Error as err:
            print("Failed to insert into table in SqLite: {}".format(err))        
 #=============================================================================            
    try:
            for e in index_Airport:
                query = "INSERT INTO Airport(AirportID, AirportCode,  LocationLat, LocationLng, CityID) VALUES ("+str(e[0])+",'"+str(e[1])+"', "+str(e[2])+", "+str(e[3])+", "+str(e[4])+");"
                cursor.execute(query)
            conn.commit()
            
            print("Inserting into Airport ==> 100%")
    except conn.Error as err:
            print("Failed to insert into table in SqLite: {}".format(err))        
  #=============================================================================    
    try:   
           for e in event:
                query = "INSERT INTO Event_(EventID , StartTime ,  EndTime , SeverityID , TypeID ,TimeZoneID ,AirportID ) VALUES ("+str(e[0])+", '"+str(e[1])+"', '"+str(e[2])+"', '"+str(e[3])+"', '"+str(e[4])+"',"+str(e[5])+","+str(e[6])+");"
                cursor.execute(query)
           conn.commit()
           
           print("Inserting into Event ==> 100%")
    except conn.Error as err:
            print("Failed to insert into table in SqLite: {}".format(err))
 #=============================================================================     
except conn.Error as err:
    print("Failed to insert into table in SqLite: {}".format(err))

cursor.close()
conn.close()
