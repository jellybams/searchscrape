from configobj import ConfigObj
from os import environ

def configer():
	"""Return a ConfigObj

	Overrides default config values with environment
	variables passed at application start
	"""

	config = ConfigObj('./config/default.cfg')
	DB_HOST = environ.get('DB_HOST')
	DB_PORT = environ.get('DB_PORT')
	GOOGLE_API_KEY = environ.get('GOOGLE_API_KEY')
	CSE_ID = environ.get('CSE_ID')

	if DB_HOST:
		config['db']['host'] = DB_HOST

	if DB_PORT:
		config['db']['port'] = DB_PORT

	if GOOGLE_API_KEY:
		config['provider']['google']['api_key'] = GOOGLE_API_KEY

	if CSE_ID:
		config['provider']['google']['cse_id'] = CSE_ID

	# TODO: use configspec to do type conversion automatically
	config['db']['port'] = int(config['db']['port'])
	config['scraper']['max_depth'] = int(config['scraper']['max_depth'])

	return config
