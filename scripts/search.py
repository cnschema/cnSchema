# -*- coding: utf-8 -*-
# author: Li Ding
#


"""
changlog
    0.0.1.20170501: task_init_en2zh_mapping init chinese mapping form 2014 translation work
"""

# base packages
import os
import sys
import json
import logging
import codecs
import hashlib
import datetime
import logging
import time
import argparse
import urlparse
import re
import collections

import requests
from elasticsearch import Elasticsearch

from cdata.core import file2abspath, any2unicode, file2json, any2sha1, any2utf8
from cdata.misc import main_subtask
from cdata.table import excel2json

from elasticsearch import Elasticsearch
from elasticsearch import helpers

"""
enable prefix autocomplete
1. add "suggest" field config in index mapping.json,  e.g.
   "properties" : {
         "suggest" : {
            "type" : "completion",
            "analyzer" : "simple",
            "search_analyzer" : "simple",
            "payloads" : true
        }
    }

2. when indexing data item, add a special field "suggest"
    item["suggest"] = {
        "input": ["term1", "term2", "the terms to be indexed"],
        "output": "term1（term2）-- the text to be displayed",
        "payload" : { "data":"additional data to be returned with output"},
    }

3. run sugest query
curl -X POST 'localhost:9200/cns_20170801/_search?pretty' -d '{
    "size":0,
    "suggest":{
        "concept-suggest" : {
            "text" : "ai",
            "completion" : {
                "field" : "index_suggest"
            }
        }
    }
}'

note: suggest/autocomplete is a prefix search
note: _suggest endpoint has been deprecated in favour of using suggest via _search endpoint. In 5.0, the _search endpoint has been optimized for suggest only search requests.

sample ES queries


    curl -X POST 'localhost:9200/cns_20170801/_suggest?pretty' -d '{
            "concept-suggest" : {
                "text" : "n",
                "completion" : {
                    "field" : "suggest"
                }
            }
    }'

    # search1
    curl -X POST 'localhost:9200/cns_20170801/_search?pretty' -d '{
            "query" : {
                "query_string" : {
                    "query" : "店",
                    "fields" : ["name", "description", "nameZh", "descriptionZh"]
                }
            }
    }'

    # search2
    curl -X POST 'localhost:9200/cns_20170801/_search?pretty' -d '{
            "query" : {
                "query_string" : {
                    "query" : "shop",
                    "fields" : ["name", "description", "nameZh", "descriptionZh", "wikidataName"]
                }
            }
    }'


    # prefix autocomplete 1
    curl -X POST 'localhost:9200/cns_20170801/_search?pretty' -d '{
        "size":0,
        "suggest":{
            "concept-suggest" : {
                "text" : "ai",
                "completion" : {
                    "field" : "index_suggest"
                }
            }
        }
    }'

    # prefix autocomplete 2
    curl -X POST 'localhost:9200/cns_20170801/_search?pretty' -d '{
        "size":0,
        "suggest":{
            "concept-suggest" : {
                "text" : "动作",
                "completion" : {
                    "field" : "index_suggest"
                }
            }
        }
    }'



"""

class CnsSearch():
    def __init__(self):
        filename = "es.cns.json"
        filename = file2abspath(filename, __file__)
        self.es_config = json.load(open(filename))
        self.conn = None

    def connect(self):
        if self.conn:
            return self.conn

        path = "{}:{}".format(self.es_config["host"], self.es_config["port"])
        logging.info(path)

        if self.es_config.get("user"):
            es = Elasticsearch([path], http_auth=(self.es_config["user"], self.es_config["pass"]))
        else:
            es = Elasticsearch([path])

        self.conn = es
        return es

    def init_mapping(self):
        """
        when install elastic search, initialize mapping for dynaic-templates

        mappingdynamic template
        https://www.elastic.co/guide/en/elasticsearch/reference/5.4/dynamic-templates.html
        es mapping -- completion
        https://www.elastic.co/guide/en/elasticsearch/reference/5.5/search-suggesters-completion.html

        python api
        https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html

        sample mapping
        https://gist.github.com/deverton/2970285
        """

        template_name = "suggest2017"
        template_filename = "estemplate.suggest.json"
        template_filename = file2abspath(template_filename, __file__)
        # logging.info(template_filename)

        with open(template_filename) as f:
            template_body = json.load(f)
        # logging.info(template_body)

        # init template
        es = self.connect()
        ret = es.indices.put_template(template_name, body=template_body)
        logging.info(ret)


    def _load_item_data(self, version):
        # load cns-core data
        filename = "../data/releases/{}/cns-core.jsonld".format(version)
        filename = file2abspath(filename, __file__)
        items = file2json(filename)["@graph"]
        logging.info(len(items))

        fileds_index_suggest = ["name","nameZh"]
        fileds_index_search = ["name","nameZh","description", "descriptionZh", "wikidataName"]
        fields_suggest_payload = ["@id", "name","nameZh", "description", "descriptionZh", "wikidataName", "wikidataUrl","wikipediaUrl"]

        es_index = self.es_config["es_index"]
        es_type = self.es_config["es_type"]

        for item in items:

            # add suggestion field
            index_suggest = []
            index_search = []
            suggest_payload = {}
            for p, v in item.items():

                if p in fields_suggest_payload:
                    suggest_payload[p] = v

                if v:
                    vx = v
                    if isinstance(v, unicode):
                        #remove markups
                        vx = re.sub(ur"<[^>]+>","",vx)

                        #remove url in description
                        vx = re.sub(ur"[hH][tT][tT][pP][s|S]?://[\S]+","",vx)

                    if p in fileds_index_suggest:
                        index_suggest.append(vx)

                    if p in fileds_index_search:
                        index_search.append(vx)

            item["id"] = any2sha1(item["@id"])
            #logging.info(item["id"])

            item["index_wildcard"] =  u"".join(index_suggest)
            item["index_search"] =  u"".join(index_search)

            if len(item["index_wildcard"])==0:
                logging.info(json.dumps(item, indent=4))
                exit()

            item["index_suggest"] = {
                "input": index_suggest,
                #"output": u"{}（{}）".format(item["name"],item["nameZh"]),
                "payload" : suggest_payload,
            }

            yield {
                "_id": item["id"],
                "_index": es_index,
                "_type": es_type,
                "_source": item
            }




    def load_data(self, version):
        """
        https://www.elastic.co/guide/en/elasticsearch/reference/5.5/search-suggesters-completion.html
        """
        es = self.connect()

        items = self._load_item_data(version)
        helpers.bulk(es, items)

        # id_field = "id"
        # es_index = self.es_config["es_index"]
        # es_type = self.es_config["es_type"]
        # for item in items:
        #     item = item['_source']
        #     logging.info(json.dumps(item, ensure_ascii=False, indent=4))
        #
        #     ret = es.index(index=es_index, doc_type=es_type, id=item[id_field], body=item)
        #     logging.info(ret)


    def es_autocomplete(self, q, size=10):
        if not q:
            return

        es = self.connect()

        ts_start = time.time()

        q = any2unicode(q)
        query = {
            "_source": ["@id","name", "nameZh"],
            "query":{
                "wildcard":{"index_wildcard":u"*{}*".format(q) }
            }
        }

        # logging.info(json.dumps(query,ensure_ascii=False))
        ret = es.search(index=self.es_config["es_index"], body=query)
        # logging.info(json.dumps(ret,ensure_ascii=False, indent=4))

        # rewrite return value
        output = {
            "results": [x["_source"] for x in ret["hits"]["hits"][:size]]
        }
        output["servertime"] = (time.time() - ts_start)
        #logging.info(json.dumps(output,ensure_ascii=False, indent=4))

        return output


    def es_search(self, q, offset=0, size=10):
        if not q:
            return
        es = self.connect()

        ts_start = time.time()

        q = any2unicode(q)
        query = {
            "_source": ["@id", "name", "nameZh", "description", "descriptionZh"],
            "query":{
                 "query_string" : {
                    #"fields" : ["name", "nameZh", "description", "descriptionZh", "wikidataName"],
                    "fields" : ["index_search"],
                    "query" : q
                }
            },
            "from": offset,
            "size": size,
        }

        # logging.info(json.dumps(query,ensure_ascii=False))
        ret = es.search(index=self.es_config["es_index"], body=query)
        # logging.info(json.dumps(ret,ensure_ascii=False, indent=4))

        # rewrite return value
        output = {
            "results": [x["_source"] for x in ret["hits"]["hits"]]
        }
        output["servertime"] = (time.time() - ts_start)
        output["total"] = ret["hits"]["total"]
        output["offset"] = offset

        #logging.info(json.dumps(output,ensure_ascii=False, indent=4))
        return output


    def es_prefix(self, q, size=10):
        if not q:
            return

        es = self.connect()

        ts_start = time.time()

        q = any2unicode(q)
        query = {
            "concept-suggest" : {
                "text" : q,
                "completion" : {
                    "field" : "index_suggest"
                }
            }
        }

        # logging.info(json.dumps(query,ensure_ascii=False))
        ret = es.suggest(index=self.es_config["es_index"], body=query)
        logging.info(json.dumps(ret, ensure_ascii=False, indent=4))

        # rewrite return value
        output = {
            "results": [x["payload"] for x in ret["concept-suggest"][0]["options"][:size]]
        }
        output["servertime"] = (time.time() - ts_start)
        #logging.info(json.dumps(output,ensure_ascii=False, indent=4))

        return output



def task_es_init_mapping(args=None):
    cns = CnsSearch()
    cns.init_mapping()

def task_es_load_data(args=None):
    cns = CnsSearch()
    version = args["version"]
    cns.load_data(version)

def task_es_test(args):
    q = args.get("input")

    cns = CnsSearch()
    es = cns.connect()

    logging.info("es_prefix")
    output = cns.es_prefix( q, size=2)
    logging.info(json.dumps(output,ensure_ascii=False, indent=4))

    logging.info("es_autocomplete")
    output = cns.es_autocomplete( q, size=2)
    logging.info(json.dumps(output,ensure_ascii=False, indent=4))

    logging.info("es_search")
    output = cns.es_search( q, size=2)
    logging.info(json.dumps(output,ensure_ascii=False, indent=4))

def task_es_test_all(args):
    cns = CnsSearch()
    es = cns.connect()

    output = cns.es_prefix( "sh", size=2)
    logging.info(json.dumps(output,ensure_ascii=False, indent=4))
    assert len(output["results"]) == 2

    output = cns.es_prefix( "tore", size=2)
    logging.info(json.dumps(output,ensure_ascii=False, indent=4))
    assert len(output["results"]) == 0

    output = cns.es_autocomplete( "tore", size=2)
    logging.info(json.dumps(output,ensure_ascii=False, indent=4))
    assert len(output["results"]) == 2

    output = cns.es_search( "tore", size=2)
    logging.info(json.dumps(output,ensure_ascii=False, indent=4))
    assert len(output["results"]) == 0

    output = cns.es_autocomplete( "美", size=2)
    logging.info(json.dumps(output,ensure_ascii=False, indent=4))
    assert len(output["results"]) == 2

    output = cns.es_search( "美", size=2)
    logging.info(json.dumps(output,ensure_ascii=False, indent=4))
    assert len(output["results"]) == 2

    output = cns.es_autocomplete( "http", size=2)
    logging.info(json.dumps(output,ensure_ascii=False, indent=4))
    assert len(output["results"]) == 1

    output = cns.es_search( "store", size=2)
    logging.info(json.dumps(output,ensure_ascii=False, indent=4))
    assert len(output["results"]) == 2
    output2 = cns.es_search( "store", offset=10, size=2)
    logging.info(json.dumps(output2,ensure_ascii=False, indent=4))
    assert len(output2["results"]) == 2
    assert output["results"][0]["@id"] != output2["results"][0]["@id"]

    output = cns.es_search( "http", size=2)
    logging.info(json.dumps(output,ensure_ascii=False, indent=4))
    assert len(output["results"]) == 1


if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.INFO)  # noqa
    logging.getLogger("requests").setLevel(logging.WARNING)

    optional_params = {
        "--input" : "search keyword",
        "--version" : "version"
    }
    main_subtask(__name__, optional_params=optional_params)

"""
    python search.py task_es_init_mapping
    python search.py task_es_load_data 3.2
    python search.py task_es_test_all
    python search.py task_es_test --input 店
    python search.py task_es_test --input 美
    python search.py task_es_test --input tore

    curl -X DELETE localhost:9200/cns_20170801

"""
