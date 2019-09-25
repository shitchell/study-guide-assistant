import re
import json
import requests

class page:
	def __init__(self, url):
		self.url = url
		self._response = None
		self.html = None
		self.terms = list()
		self.load()

	def load(self):
		self._response = requests.get(self.url)
		self.html = self._response.text
		self._load_terms()

	def _load_terms(self):
		page_data = re.findall("<script> window\.Quizlet\.setPageData = (.*?); QLoad\('Quizlet\.setPageData'\); </script>", self.html)
		if page_data:
			self.terms = list()
			page_data = json.loads(page_data[0])
			for key in page_data['termIdToTermsMap']:
				term_data = page_data['termIdToTermsMap'][key]
				term = page.term(term_data['word'], term_data['definition'], term_data['lastModified'])
				self.terms.append(term)

	class term:
		def __init__(self, term, definition, timestamp):
			self.term = term
			self.term_short = term[:20] + "..." if len(term) > 20 else term
			self.definition = definition
			self.timestamp = timestamp

		def __repr__(self):
			return self.__str__()
		
		def __str__(self):
			return str(self.__class__)[8:-2] + ": " + self.term_short.replace('\n', ' ')