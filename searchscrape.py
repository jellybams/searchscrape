import json
from config import configer, getargs, getlogger
from mongoengine import connect
from services.search import Gsearch
from services.scrape import ScraperQueue
import sys

config = configer()
args = getargs()
logger = getlogger()

connect(config['db']['db'], host=config['db']
        ['host'], port=config['db']['port'])

search_term = args.search_term
logger.info('starting google search and link scrape for: ' + search_term)
sq = ScraperQueue(search_term=search_term)
gsearch = Gsearch(api_key=config['provider']['google']['api_key'],
                  cse_id=config['provider']['google']['cse_id'])

start = 1
retries = 0
while sq.queue_size() < 20:
    results = gsearch.query(search_term, start)
    if results is not None:
    	sq.enqueue(results['items'], None)
    	start = results['queries']['nextPage'][0]['startIndex']
    else:
    	logger.error('did not get a response from google')
    	retries += 1

    if retries == 10:
    	logger.error('reached max retries')
    	sys.exit()


# -----
# with open('./tmp/results.json') as data_file:
#     logger.info('loading json')
#     results = json.load(data_file)
# sq.enqueue(results['items'], None)
# -----

sq.run(config['scraper']['max_depth'])
