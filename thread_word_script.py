import basc_py4chan
import time

import requests
import json
import urllib2
import re
import operator
import random
import MySQLdb
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize,word_tokenize



#here we comment what board we want to start looking at
board = basc_py4chan.Board('pol')


thread_ids = board.get_all_thread_ids()

str_thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
#print('There are', len(str_thread_ids), 'active threads on /tg/:', ', '.join(str_thread_ids))
#str_thread_ids just lists out every active thread currently on tv



for x in str_thread_ids:
    api_4chan = 'https://a.4cdn.org/pol/thread/%s.json' % (x)
    #here we just build out the api list to start collecting some data
    print api_4chan

    #build the link just for reference
    link_4chan = 'http://boards.4chan.org/pol/thread/%s' % (x)

    req = urllib2.Request(api_4chan)
    opener = urllib2.build_opener()
    f = opener.open(req)
    json_z = json.loads(f.read())
    #print json_z

    thread_comments = (json.dumps(json_z['posts'][0]['com'], indent=3, sort_keys=True))
    total_reply_count = int(json.dumps(json_z['posts'][0]['replies'], indent=3, sort_keys=True))

    print total_reply_count

    thread_text = []
    for comment_num in range(0,total_reply_count):
        try:
            thread_comment = (json.dumps(json_z['posts'][comment_num]['com'], indent=3, sort_keys=True))
            soup = BeautifulSoup(thread_comment)
            text = soup.get_text()
	    print text
	
	    sentence_build = word_tokenize(str(text))
            print sentence_build
            time.sleep(1)

            #thread_text.append(text)
            #print "---------------------------------------------"
            #print "gogo"
            #print text[0:3]
            #print "gogo"
            #print "---------------------------------------------"
            #print thread_text
        except KeyError:
            pass


    	time.sleep(3)



    #try:

        #print thread_comments
   # except ValueError as e:
        #pass


    #for item in json_z:
        #print item
        #time.sleep(.1)


