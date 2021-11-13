from datetime import datetime

from elasticsearch import Elasticsearch

es = Elasticsearch([{
    'host': 'localhost',
    'port': 9202
    }])


res = es.search(index="test-index", query={
    "match_all": {}
    })
