from BeautifulSoup import BeautifulSoup
import re, sys, os, urllib2, time
import oauth2 as oauth
import json

if len(sys.argv) != 3:
	print 'USAGE: python storyline.py <cricketer name> <json file>'
	sys.exit(1)

cricketer = sys.argv[1]
outfile = sys.argv[2]

mon_dict = {
 'jan': 1,
 'feb': 2,
 'mar': 3,
 'apr': 4,
 'may': 5,
 'jun': 6,
 'jul': 7,
 'aug': 8,
 'sep': 9,
 'oct': 10,
 'nov': 11,
 'dec': 12
}

os.environ['http_proxy']="http://tgandhi:zodiac@proxy.iitk.ac.in:3128/"
OAUTH_CONSUMER_KEY = "dj0yJmk9YWF3ODdGNWZPYjg2JmQ9WVdrOWVsWlZNRk5KTldFbWNHbzlNVEEyTURFNU1qWXkmcz1jb25zdW1lcnNlY3JldCZ4PTUz"
OAUTH_CONSUMER_SECRET = "a3d93853ba3bad8a99a175e8ffa90a702cd08cfa"

def oauth_request(url, params, method="GET"):
    # Removed trailing commas here - they make a difference.
    params['oauth_version'] = "1.0" #,
    params['oauth_nonce'] = oauth.generate_nonce() #,
    params['oauth_timestamp'] = int(time.time())

    consumer = oauth.Consumer(key=OAUTH_CONSUMER_KEY,
                              secret=OAUTH_CONSUMER_SECRET)
    params['oauth_consumer_key'] = consumer.key
    req = oauth.Request(method=method, url=url, parameters=params)
    req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, None)
    return req	

def get_results(qtype,keyword):
    url = "http://yboss.yahooapis.com/ysearch/"+qtype

    req = oauth_request(url, params={"q": keyword, "format": "json"})
    # This one is a bit nasty. Apparently the BOSS API does not like
    # "+" in its URLs so you have to replace "%20" manually.
    # Not sure if the API should be expected to accept either.
    # Not sure why to_url does not just return %20 instead...
    # Also, oauth2.Request seems to store parameters as unicode and forget
    # to encode to utf8 prior to percentage encoding them in its to_url
    # method. However, it's handled correctly for generating signatures.
    # to_url fails when query parameters contain non-ASCII characters. To
    # work around, manually utf8 encode the request parameters.
    req['q'] = req['q'].encode('utf8')
    req_url = req.to_url().replace('+', '%20')
    #print req_url
    #http = urllib3.PoolManager(10)
    #r1 = http.request('GET', req_url)
    page = urllib2.urlopen(req_url)
    json_txt = page.read()
    return json_txt


def get_dm(headline):
	month = ""
	headline = headline.lower()
	matchobj = re.search('(\\d{4})',headline)
	if matchobj==None:
		print 'Exception!! year not found'
		print headline
		sys.exit(1)	
	year = matchobj.groups(0)[0]
	ks = mon_dict.keys()
	ks.sort(key=lambda x:mon_dict[x])
	cur_match_pos = 1111
	for mon in ks:
		match_pos = headline.find(mon) 
		if match_pos >= 0 and match_pos < cur_match_pos:
			month=mon
			cur_match_pos = match_pos
	#if month is None:
	#	print 'Exception!! month not found'
	#	print headline
	#	sys.exit(1)
	return  year+","+str(mon_dict.get(month,''))
			
json_txt = get_results('web',cricketer+" cricinfo")
json_ob     = json.loads(json_txt)
#import pprint;pprint.pprint(twitter_json)
json_ob = json_ob['bossresponse']
qtype = 'web'
cricinfo_url =""
if json_ob[qtype].has_key('results'):
	for result in json_ob[qtype]['results']:
		if not result['url'].find('cricinfo') >= 0:
			continue
		cricinfo_url= result['url']
		print 'Got cricinfo url'
		break
if cricinfo_url=="":
	print 'ERROR'
	sys.exit(1)
cricinfo_url += '?index=timeline'
page = urllib2.urlopen(cricinfo_url)
#print cricinfo_url
soup=BeautifulSoup(page)

### Fetch titles #########
titles=[]
for item in soup.fetch('span',{'class':'ciPhotoWidgetLink'}):
	titles.append(item)

if len(titles)==0:
	print 'ERROR'
	sys.exit(1)

titles=titles[1:]

if len(titles)==0:
	print 'ERROR'
	sys.exit(1)


no_events = len(titles)
res_obj   = {  'timeline': { 
	           'headline': 'Timeline for %s' % cricketer, 
	           'type': "default" , 
	           'text': "The Awesome hack!!", 
	           'date':[ ]
	             } 
	      }
### Fetch time of events #########
for i in range(1,no_events+1):
	e = soup.fetch('div',{'id': 'playertimeline'+str(i)+'-title'})[0]
	desc1 = soup.fetch('div',\
                        {'id': 'playertimeline'+str(i),
                         'class' : 'rhboxtimeline'})[0]
	desc = re.sub("'", "\\'",desc1.renderContents())
	desc = "'" + desc + "'"
	#print desc
	dm = get_dm(e.renderContents())
	l = {'startDate': dm, 
	     'headline' : titles[i-1].text,
             'text' : desc, 
					 'asset' : {
						         'media': '',
						         'credit':'',
						         'caption':''
						       }
            }
        res_obj['timeline']['date'].append(l)

fp=open(outfile,'w')
fp.write(json.dumps(res_obj))
fp.close()
sys.exit(0)
