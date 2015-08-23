# google search result scraper

To run, two things must happen:

1. Install requirements via pip with `pip install -r requirements.txt`

2. The `GOOGLE_API_KEY` and `CSE_ID` environment variables must be set. This can be done when executing the script via:

```shell
$ GOOGLE_API_KEY=<your api key> CSE_ID=<your search engine id> python searchscrape.py -q "search term"
```

