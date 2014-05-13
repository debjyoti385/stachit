import urllib, urllib2, sys, re
import json
from numpy import double
import os,pprint

os.environ['http_proxy']="http://tgandhi:zodiac@proxy.iitk.ac.in:3128/"

if len(sys.argv) != 2:
	print 'Usage: python cap_test.py "text to analyze"'
	sys.exit(1)

query = sys.argv[1]
cap_query = re.sub("'","\\'",query)

cap_query  = urllib.quote(cap_query)
cap_url    = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20contentanalysis.analyze%20where%20text%3D%27'+cap_query+\
            '%27%3B&diagnostics=true&format=json&'
page=urllib2.urlopen(cap_url)
json_ob = json.loads(page.read())
#print pprint.pprint(json_ob)
#pprint.pprint(json.loads(r1.data))
n_results = json_ob['query']['count']
if n_results > 0:
    results = []
    entity_ls = json_ob['query']['results']['entities']['entity']
    if type(entity_ls)==type({}):
        entity_ls = [entity_ls]
    for e in entity_ls:
        #print e
        results.append((double(e['score']),e['text']['content']))
    results.sort()
    results.reverse()
    for e in results:
        #print e[1],e[0]
        print e[1]
    
	

