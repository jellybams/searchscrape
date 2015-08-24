from lxml import html, etree
from config import getlogger
from collections import deque
from datetime import datetime
from urlparse import urlparse, urljoin
from models.page import Page
import requests

logger = getlogger()


class PageScraper:
    depth = 0

    def run(self, page):
        """
        Get all the links from `page['link']`
        """

        logger.info('getting contents of %s', page['link'])
        try:
            res = requests.get(page['link'])
        except requests.exceptions.RequestException as e:
            logger.error(e)

        tree = html.fromstring(res.text) if res.text else etree.Element("root")
        ret = {
            'link': page['link'],
            'links': [],
            'title': tree.findtext('.//title')
        }

        url_parts = urlparse(page['link'])
        for item in tree.xpath('//body//a'):
            child_page = {
                'link': item.get('href'),
                'text': item.text.strip() if item.text else '',
                'parent': page['parent']
            }

            if child_page['link']:
                link_parts = urlparse(child_page['link'])

                # handle relative links
                if bool(link_parts.netloc) is False:
                    child_page['link'] = urljoin(
                        page['link'], child_page['link'])
                # handle missing protocol
                elif bool(link_parts.scheme) is False:
                    child_page['link'] = url_parts.scheme + \
                        ':' + child_page['link']

                # only crawl pages available over http(s)
                if urlparse(child_page['link']).scheme in ['http', 'https']:
                    # print "adding url to queue: " + child_page['link'] + '\n'
                    ret['links'].append(child_page)
        return ret


class ScraperQueue:
    search_term = None
    curr_parent = None
    pending = deque([])
    scraper = PageScraper()

    def __init__(self, **kwargs):
        self.search_term = kwargs['search_term']

    def queue_size(self):
        return len(self.pending)

    def enqueue(self, items, parent):
        logger.info(
            'adding ' + str(len(items)) + ' with parent ' + str(parent) + ' to scrape queue')
        for item in items:
            self.pending.append({
                'link': item['link'],
                'text': item['text'] if 'text' in item else None,
                'search_term': self.search_term,
                'links': [],
                'parent': parent
            })

    def run(self, max_depth):
        depth = 0
        while len(self.pending) > 0:
            page = self.pending.popleft()

            # get links for the current page
            page_data = self.scraper.run(page)

            page['title'] = page_data['title']
            page['links'] = page_data['links']

            # persist to db
            instance = Page(title=page['title'],
                            url=page['link'],
                            search_term=self.search_term,
                            links=page['links'],
                            created_at=datetime.now(),
                            updated_at=datetime.now())
            if page['parent'] is not None:
                instance.parent = page['parent']
            instance.save()

            if self.curr_parent is None or page['parent'] is not self.curr_parent:
                parent_id = self.curr_parent

                if parent_id is None:
                    parent_id = instance.id

                if page['parent'] is not self.curr_parent:
                    depth += 1
                    parent_id = instance.id
                    self.curr_parent = page['parent']

            logger.info('crawl level: %d, max depth: %d, queue size: %d',
                        depth, max_depth, len(self.pending))
            logger.info(
                'crawling page id %s, url: %s', str(instance.id), page['link'])

            # queue up the links for another level of crawling
            if depth < max_depth:
                self.enqueue(page_data['links'], parent_id)
