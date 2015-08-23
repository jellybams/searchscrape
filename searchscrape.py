from config import configer, getargs
from mongoengine import connect
from services.search import Gsearch
from services.scrape import ScraperQueue

config = configer()
args = getargs()

connect(config['db']['db'], host=config['db']
        ['host'], port=config['db']['port'])

search_term = args.search_term
print "starting google search and link scrape for: " + search_term
sq = ScraperQueue(search_term=search_term)
gsearch = Gsearch(api_key=config['provider']['google']['api_key'],
                  cse_id=config['provider']['google']['cse_id'])

start = 1
while sq.queue_size() < 20:
    results = gsearch.query(search_term, start)
    sq.enqueue(results['items'], None)
    start = results['queries']['nextPage'][0]['startIndex']

sq.run(config['scraper']['max_depth'])
