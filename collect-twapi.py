# -*- coding: utf-8 -*-
import io
import json
from TwitterAPI import TwitterAPI
import os
import re
#####script uses --twitterAPI--

#twitter api keys

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN_KEY = ""
ACCESS_TOKEN_SECRET = ""
api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)





print("Enter Search Terms (may be delimited with commas")
QUERY = input()
if '#' in QUERY:
    QUERY.replace("#","")
else:
    pass

search_terms = QUERY.split(',')

if "#" in search_terms:
    search_terms.replace("#","")
else:
    pass
search_term_map = {}
os.chdir("terms/")
#hashmaps. each search term is given its own json file
for search_term in search_terms:
    stm = {
        'input_fp': ".".join([search_term, 'json']),
        'output_fp': ".".join([search_term + '_processed', 'json'])
    }
    search_term_map[search_term] = stm

def ke(x):
	try:
		if 'text' in x:
			return str(x['text'])
		else:
			return " "
	except:
		return " "

r = api.request('statuses/filter', {'track': QUERY})



n = 0
print('Filtering the public timeline for ' + QUERY)
def main():
	global n
	global r
	dummy = 0
	tk = []
	filtered = {}
	for tweet in r:
		filtered = {}
		data = json.loads(json.dumps(tweet, ensure_ascii=False))
		n = n + 1
		nn = str(n) + " "
		dummy = dummy + 1
		for k, value in search_term_map.items() :
			if re.search(k,ke(data),re.IGNORECASE) is not None:
				try:
					######NOTE: this is a windows C hack that bypasses the hard drive's cache so it is constantly writing to disk
					######for example: 3TB WD drives with a 64mb cache 
					fh = os.open(search_term_map[k]['output_fp'],os.O_CREAT|os.O_APPEND|os.O_BINARY|os.O_RDWR)
					
					
					#ID UNIQUE KEY IF ANY
					try:
						id = tweet['id_str']
					except KeyError:
						id = dummy
					filtered['id_str'] = id
					
					#find handle
					try:
						sn = tweet['user']['screen_name']
					except KeyError:
						sn = ""
					filtered['screen_name'] = sn

					#find time created
					try:
						twtime = tweet['created_at']
					except KeyError:
						twtime = ""
					filtered['created_at'] = twtime
					
					#find text
					try:
						txt = tweet['retweeted_status']['text']
						RT = True
					except KeyError:
						txt = tweet['text']
						RT = False
					filtered['text'] = txt
					filtered['RT'] = RT
					
					#find account creation date
					try:
						userDate = tweet['user']['created_at']
					except KeyError:
						userDate = ""
					filtered['account_date'] = userDate

					#find bio info
					try:
						bio = tweet['user']['description']
					except KeyError:
						bio = ""
					filtered['bio'] = bio

						#get followers
					try:
						foll = tweet['user']['followers_count']
					except KeyError:
						foll = 0
					filtered['followers'] = foll
					
					#get following
					try:
						following = tweet['user']['friends_count']
					except KeyError:
						following = 0
					filtered['following'] = following

					#get language
					try:
						ln = tweet['lang']
					except KeyError:
						ln = 0
					filtered['lang'] = ln
					#get location
					try:
						if tweet['coordinates'] is not None:
							loc = tweet['coordinates']['coordinates']
						else:
							loc = []
					except KeyError:
						pass
					filtered['loc'] = loc
					
					os.write(fh,bytes(u'{0}\n'.format(json.dumps(filtered, ensure_ascii=False)),'utf-8',errors='ignore'))
					os.fsync(fh)
					print(nn + tweet['user']['screen_name']  + "	" +    str(tweet['text'][:130].encode('utf-8').decode('ascii', 'ignore')), flush=True)
					os.close(fh)
	                                ####these controls will break the program after ~2000 registered tweets that have been captured by the program
				except:
					break
			else:
				break
		else:
			break

while True:
		main()
