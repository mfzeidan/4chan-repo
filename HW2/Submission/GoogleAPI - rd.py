# -*- coding: utf-8 -*-
"""
Created on Sun Feb 07 11:24:28 2016

@author: Mz
"""


"""
Select any 10 McDonald’s in New York and the associated stores that are within 100 miles of them
Determine route distance (in KM) for each pair of those McDonald’s (hint use google maps distance matrix)
Save the following results in a datatable:  the two stores, each stores lat and lon, the haversine distance between the two stores, and the route distance between the two stores

"""

# import the following libraries
import json, urllib, sqlite3, csv, math, json, urllib

myConnection = sqlite3.connect('mc250.db')
myCursor = myConnection.cursor()

myFile = open('mcdonalds_250.csv', 'rt')
myReader = csv.reader(myFile)

sqlString = """ 
            CREATE TABLE IF NOT EXISTS mcdonalds_time
            (Store1 TEXT,
            Store2 TEXT,
            Store1Lat INT,
            Store1Lon INT,
            Store2Lat INT,
            Store2Lon INT,
            Haversine INT,
            googletime INT);"""
 
myCursor.execute(sqlString)
myConnection.commit()
myConnection.close
#           
#for row in myReader:
#    myCursor.execute('INSERT INTO mcdonalds_time VALUES (?,?,?,?,?,?,?,?);', tuple(row))
#    myConnection.commit()

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees).
    Source: http://gis.stackexchange.com/a/56589/15183
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    km = (6367 * c) * 0.621371 # i translated this to miles but was too lazy to change the variable
    return km

def googleapi(lon1,lat1,lon2,lat2):
    """do the api code through this since python wont do as I say"""
    original_coordinates = lat1,lon1
    destination_coordinates = lat2,lon2
    url = 'http://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&mode=driving&language=en-EN&sensor=false'%(str(original_coordinates),str(destination_coordinates))
    result= json.load(urllib.urlopen(url))
    driving_time = result['rows'][0]['elements'][0]['duration']['value']
    print driving_time



#   0        1        2          3         4           5
# store1, store2, store1lat, store1lon, store2lat, store2lon
haversineRow = []
for row in myReader:
    distance = haversine(float(row[3]), float(row[2]), float(row[5]), float(row[4]))
    lat1 =  "%s" % row[2]
    lon1 =  "%s" % row[3]
    lat2 =  "%s" % row[4]
    lon2 =  "%s" % row[5]
    latlon1 = lat1+ ',' +lon1 
    latlon2 = lat2+ ',' + lon2   
    orig_coord = latlon1
    dest_coord = latlon2
    url = 'http://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&mode=driving&language=en-EN&sensor=false' % ((orig_coord),(dest_coord))
    result= json.load(urllib.urlopen(url))
    print result    
    driving_time = result['rows'][0]['elements'][0]['duration']['value']
    print driving_time


    #print 'haversine: ' + str(distance)
    #print 'store num: ' + row[1]
    #print row
    #print str(latlon1)
    

    #haversineRow.append((row[0], row[1], row[2], row[3], row[4], row[5], distance, driving_time))
    #print haversineRow


#updatedSQLmcd = """
#            CREATE TABLE IF NOT EXISTS mcdInfo 
#            (store1 INT,
#            store2 INT,
#            store1Lat FLOAT,
#            store1lon FLOAT,
#            store2lat FLOAT,
#            store2lon FLOAT,
#            haversine FLOAT,
#            drivingtime INT)
#            """
##            
#myCursor.execute(updatedSQLmcd)
##myConnection.commit()
##
#insertSQLmcd = "INSERT INTO mcdInfo VALUES (?,?,?,?,?,?,?,?)"
#myCursor.executemany(insertSQLmcd, haversineRow)
#myConnection.commit()   

    
  



    

#    
#    for el in result['rows'][0]['elements']:
#        print 'seconds:=', el['duration']['value'], 'meters:=', el['distance']['value']  
    
    #original_coord = [(row[2]), (row(3))]
    #print original_coord
#    orig_coord = (float(row[2]), float(row[3]))
#    dest_coord = (float(row[4]), float(row[5])
    #api = 'http://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&mode=driving&language=en-EN&sensor=false' % (str(orig_coord), str(dest_coord))
    #result = json.load(urllib.urlopen(api))
    #driving_time = result['rows'][0]['elements'][0]['duration']['value']

#    print route_distance
#    print driving_time
    
    

myCursor.close()
myConnection.close()
myFile.close()
myReader = None
    
        
#this is how you call a single pair (point to point)
#orig_coord = '40.5809172,-74.1691334'
#dest_coord = '45.44413,-122.628791'
#dest_coord = '45.44413,-122.628791|39.08746,-84.519881'


#url = 'http://maps.googleapis.com/maps/api/distancematrix/json?origins=%s'\
#      '&destinations=%s&mode=driving&language=en-EN&sensor=false'\
#       % (str(orig_coord), str(dest_coord))
#result= json.load(urllib.urlopen(url))
#driving_time = result['rows'][0]['elements'][0]['duration']['value']
#print 'seconds:= ', driving_time

