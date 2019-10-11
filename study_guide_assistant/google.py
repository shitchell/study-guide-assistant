import os
import json
import requests
import urllib.parse

_key_filepath = "/etc/google/search_api.key"
_cx_filepath = "/etc/google/search_api.cx"
_key = None
_cx = None

def load_key(filepath):
	global _key
	_key = open(filepath).read().strip()

def load_cx(filepath):
	global _cx
	_cx = open(filepath).read().strip()

def search(query, key=None, cx=None, stop=3):
	if key == None:
		if _key == None:
			raise APIKeyRequired
		key = _key
	if cx == None:
		if _cx == None:
			raise APICXRequired
		cx = _cx
	
	url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s" % (urllib.parse.quote(key), urllib.parse.quote(cx), urllib.parse.quote(query))
	res = requests.get(url)
	try:
		res = json.loads(res.text)
		return [x['link'] for x in res['items']][:stop]
	except:
		pass

class APIKeyRequired(Exception): pass
class APICXRequired(Exception): pass

load_key(_key_filepath)
load_cx(_cx_filepath)