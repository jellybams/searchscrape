import requests

class Gsearch:
	"""Abstraction over Google Custom Search API"""

	base_url = 'https://www.googleapis.com/customsearch/v1'
	api_key = None
	cse_id = None

	def __init__(self, api_key, cse_id, **kwargs):
		if not api_key or not cse_id:
			raise ValueError('An api_key and cse_id is required.')

		self.api_key = api_key
		self.cse_id = cse_id

		if hasattr(kwargs, 'url'):
			self.base_url = kwargs['url']

	def query(self, phrase, start_idx):
		"""Exectute a query for the given search phrase"""

		payload = {
			'key': self.api_key,
			'cx': self.cse_id,
			'q': phrase,
			'start': start_idx
		}

		print payload

		r = requests.get(self.base_url, params=payload)
		return r.json()
