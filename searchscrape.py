import argparse
import json
from config import configer
from mongoengine import connect
from services.search import Gsearch
from services.scrape import ScraperQueue

from pprint import pprint

# argument parsing to get search term
parser = argparse.ArgumentParser(description='Search google and scrape links from first 20 results.')
parser.add_argument('-q', '--query', dest='search_term', action='store',
   default='', help='the term to search google for', required=True)
args = parser.parse_args()

config = configer()
connect(config['db']['db'], host=config['db']['host'], port=config['db']['port'])
search_term = args.search_term;

sq = ScraperQueue(search_term=search_term)
gsearch = Gsearch(api_key=config['provider']['google']['api_key'],
	cse_id=config['provider']['google']['cse_id'])

start = 1
while sq.queue_size() < 20:
	print "q size: " + str(sq.queue_size())
	results = gsearch.query(search_term, start)
	sq.enqueue(results['items'], None)
	start = results['queries']['nextPage'][0]['startIndex']

sq.enqueue(results['items'], None)
sq.run(config['scraper']['max_depth'])
