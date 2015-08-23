import json
import uuid
from collections import deque
from config import configer
from datetime import datetime
from services.search import Gsearch
from services.scrape import PageScraper

from pprint import pprint

config = configer()
search_term = 'test'
scraper = PageScraper()
to_scrape = deque([])

res = scraper.run('http://stackoverflow.com/questions/2632677/python-integer-incrementing-with')

# pprint(res)
