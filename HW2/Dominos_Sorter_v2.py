# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 12:18:35 2016

@author: Mz
"""

from bs4 import BeautifulSoup

import re

# # Root dominos link to parse through
from bs4 import BeautifulSoup
import requests
import re
import sqlite3

def dominoes():
    
    db = 'dominos.db'
    myConnection=sqlite3.connect(db)
    myCursor = myConnection.cursor()
    createSQLTable = '''CREATE TABLE IF NOT EXISTS dominos
    (state text,
    city text,
    store_num text,
    url text);'''
    myCursor.execute(createSQLTable)
    myConnection.commit()
    myCursor.close()
    
    # # Root dominos link to parse through
    rootURL = 'http://www.menuism.com/restaurant-locations/dominos-pizza-7144/us'
    r = requests.get(rootURL)
    soup = BeautifulSoup(r.content)
    templist = []
    # Get state urls from the root URL
    # Store in stateURL List
    state_url_list = []
    storeUrlList = soup.select('.popular-cities-box li a')
    for tags in storeUrlList:
       URLlink =  (tags['href'])
       d_page = requests.get(URLlink)
       soup = BeautifulSoup(d_page.content)
       stateStoreList = []
       storeState = soup.select('.list-unstyled-links a')
       
       #print tags
       
       # this is a mess but this is my way of getting state and city from the original regex :)
       
       for stores in storeState:
           storeNumRegex = re.compile(r'\d\d\d\d\d\d')
           mo = storeNumRegex.search(str(stores))
           if mo is None:
               continue
           cityAndStateRegex = re.compile(r' in(.*?) -')
           if cityAndStateRegex is None:
               continue
           cas_mo = cityAndStateRegex.search(str(stores))
           info = cas_mo.group()
           newinfo = info.replace('in','')
           thenewinfo = newinfo.replace('-','')
           #print thenewinfo
           cityRegex = re.compile('^(.+?),')
           city_mo = cityRegex.search(str(thenewinfo))
           city = city_mo.group().replace(',','')
           #print city
           stateRegex = re.compile('\s(\w)$')
           state_mo = stateRegex.search(str(thenewinfo))
           #print thenewinfo
           
           state = thenewinfo[-3:]
           #print state
           #print "2" + state_mo.group()
           
           
           #print info
           st = str(info.split()[2])
           
           #state = st.replace(',','')
           #print state
           
           
           #print city
           
           store_num = mo.group()
           
           store_link = stores['href']
           
           
           #print state, city, store_num, store_link
           templist.append((state,city,store_num,store_link))
           #print len(templist)
           if len(templist) == 6412:
               myCursor = myConnection.cursor()
               myCursor.executemany('INSERT INTO dominos VALUES (?,?,?,?);',templist)
               myConnection.commit()
               myCursor.close()

dominoes()
     