import basc_py4chan
import time

import requests
import json
import urllib2
import re
import operator
import random
import MySQLdb



while True:

	board = basc_py4chan.Board('sp')
	thread_ids = board.get_all_thread_ids()
	str_thread_ids = [str(id) for id in thread_ids]  # need to do this so str.join below works
	#print('There are', len(str_thread_ids), 'active threads on /tg/:', ', '.join(str_thread_ids))
	overall_dict = {}
	#print str_thread_ids
	overall_dict = {}
	con = MySQLdb.connect(host='127.0.0.1', port=3306,
						  user='root',
						  passwd='Krvcp2Vn5f',
						  db='4chan_test')
	cur = con.cursor()




	try:
		for x in str_thread_ids:
			api_4chan = 'https://a.4cdn.org/sp/thread/%s.json' % (x)
			link_4chan = 'http://boards.4chan.org/sp/thread/%s' % (x)
			print api_4chan
			print link_4chan

			req = urllib2.Request(api_4chan)
			opener = urllib2.build_opener()
			f = opener.open(req)
			json_z = json.loads(f.read())
			total_reply_count = int(json.dumps(json_z['posts'][0]['replies'], indent=3, sort_keys=True))

			thread_list = []

			for i in range(0, total_reply_count):
				# print i
				try:
					text_to_print = json.dumps(json_z['posts'][i]['com'], indent=3, sort_keys=True)
				except KeyError:
					pass
				try:
					# print text_to_print
					if "#p" in text_to_print:
						# m = re.search('(?<=-)\w+'
						reference = text_to_print[13:21]
						# print reference
						# if reference not in thread_list:
						thread_list.append(reference)
						# print(thread_list)
				except KeyError,NameError:
					pass

			counter_dict = {}

			for x in thread_list:
				# print x
				# print thread_list.count(x)
				# print "------"
				counter_dict[x] = thread_list.count(x)

			# print counter_dict
			#print counter_dict

			try:
				maximum = max(counter_dict, key=counter_dict.get)
				values = (maximum, counter_dict[maximum])

				print "-------------"
				#print(maximum, counter_dict[maximum])
				#print values
		###adding top keys to a dictionary

				new_link = link_4chan + '#p' + '%s' % maximum
				#print new_link

				overall_dict[new_link]=counter_dict[maximum]
				#print overall_dict
			except ValueError:
				pass
			#print overall_dict

			sleep_time = random.random()
			time.sleep(sleep_time +4)
	except Exception:
		pass


	x = overall_dict
	sorted_x = sorted(x.items(), key=operator.itemgetter(1),reverse=True)
	#saveFile = open('polthreads.csv','w')
	#saveFile.write(sorted_x)
	#saveFile.close()
	#print x
	#print sorted_x

	for x,y in sorted_x:
		print x,y
		print 'link'


	def json_list(list):
		lst = []
		for pn in list:
			d = {}
			d['link']=pn
			lst.append(d)
		return json.dumps(lst)

	lists = json_list(sorted_x)

	print lists

	sql_statement = """UPDATE json_carry set json = %s WHERE board = 'sp'"""

	#try:
	cur.execute("""UPDATE json_carry set json = '%s' WHERE board = 'sp'""" % lists)		
	con.commit()
		#print "sql updated!"
	#except:
		#con.rollback()

	con.close()


