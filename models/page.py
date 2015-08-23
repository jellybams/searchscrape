from mongoengine import *


class Page(Document):
    title = StringField()
    url = StringField()
    search_term = StringField()
    links = ListField(DictField())
    parent = ObjectIdField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    meta = {
    	'collection': 'page_links',
        'indexes': [
            'title',
            'search_term'
        ]
    }
