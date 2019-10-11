#!/usr/bin/env python3

# It's servers all the way down
from bottle import route, run, install, response, request, ServerAdapter, static_file
from cheroot.ssl.builtin import BuiltinSSLAdapter
from cheroot import wsgi
import ssl
import pkgutil
import os

# Search imports
from google import search
import quizlet
import string
import json
import re

# Enable cors
class EnableCors(object):
	name = 'enable_cors'
	api = 2

	def apply(self, fn, context):
		def _enable_cors(*args, **kwargs):
			response.headers['Access-Control-Allow-Origin'] = '*'
			response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
			response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

			if request.method != 'OPTIONS':
				return fn(*args, **kwargs)

		return _enable_cors

# Enable ssl
class SSLServer(ServerAdapter):
	def run(self, handler):
		server = wsgi.Server((self.host, self.port), handler)
		chain = "/etc/letsencrypt/live/quizlet.shitchell.com/fullchain.pem"
		cert = "/etc/letsencrypt/live/quizlet.shitchell.com/cert.pem"
		key = "/etc/letsencrypt/live/quizlet.shitchell.com/privkey.pem"
		server.ssl_adapter = BuiltinSSLAdapter(cert, key, chain)

		# By default, the server will allow negotiations with old protocols,
		# so we only allow TLSv1.2
		server.ssl_adapter.context.options |= ssl.OP_NO_TLSv1
		server.ssl_adapter.context.options |= ssl.OP_NO_TLSv1_1

		try:
			server.start()
		finally:
			server.stop()

# Searchify
def quizlet_search(query, max_results=3):
	response = {
		"query": query,
		"exact": True,
		"results": []
	}
	query = simplify_string(query)
	results = search('"%s"' % query, stop=max_results)
	if not results:
		results = search('%s' % query, stop=max_results)
		response['exact'] = False
	for url in results:
		quizlet_page = quizlet.Page(url)
		for term in quizlet_page.terms:
			if query in simplify_string(term.term):
				term_dict = {
					"term": term.term,
					"definition": term.definition,
					"timestamp": term.timestamp,
					"ref": quizlet_page.url
				}
				response['results'].append(term_dict)
	return response

# Simplify strings (yay helpful comments!)
def simplify_string(s):
	# Uppercase = lowercase
	s = s.lower()
	# Punctuation = 
	s = s.translate(str.maketrans('', '', string.punctuation))
	# Whitespace = space space
	s = " ".join(s.split())
	return s.strip()

# Package relative static filepaths
def _static_file(filepath):
	package_filepath = os.path.dirname(os.path.abspath(__file__))
	return static_file("htdocs/" + filepath, package_filepath)

@route('/')
def do_index():
	return 'one comes after two.'

@route('/search')
def do_search():
	query = request.query.q
	try:
		max_results = int(request.query.results)
	except:
		max_results = 3
	max_results = min(10, max_results)
	return json.dumps(quizlet_search(query, max_results))

@route('/sample/demo')
def do_demo():
	return _static_file("sample.html")

@route('/sample/quiz')
def do_quiz():
    return _static_file("demo.html")

@route('/static/<path:path>')
def do_static(path):
	return _static_file("static/" + path)

if __name__ == "__main__":
	install(EnableCors())
	run(host='0.0.0.0', port=9001, debug=True, server=SSLServer)