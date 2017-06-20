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
import wikipedia

from cdata.misc import main_subtask

def task_wikify(args):
    #logging.info(args)
    ret = wikify(args["phrase"])
    logging.info(json.dumps(ret,sort_keys=True, indent=4))

MAX_RESULT = 1
def wikify(phrase, description=None):
    ret = {}
    ret.update(wikify1(phrase, description))
    ret.update(wikify3(phrase, description))
    return ret

def wikify1(phrase, description=None):

    #wikification
    """
    {
        searchinfo: - {
        search: "birthday"
        },
        search: - [
        - {
            repository: "",
            id: "P3150",
            concepturi: "http://www.wikidata.org/entity/P3150",
            url: "//www.wikidata.org/wiki/Property:P3150",
            title: "Property:P3150",
            pageid: 28754653,
            datatype: "wikibase-item",
            label: "birthday",
            description: "item for day and month on which the subject was born. Used when full "date of birth" (P569) isn't known.",
            match: - {
            type: "label",
            language: "en",
            text: "birthday"
        }
    },"""
    urlBase = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search={}&format=json&language=en&uselang=en&type=property"
    url = urlBase.format(re.sub("\s+","%20",phrase))
    r = requests.get(url)
    items = json.loads(r.content).get("search",[])
    #logging.info(items)
    ret = {}
    for idx, item in enumerate(items[0:MAX_RESULT]):
        if idx > 0:
            prefix = "wikidata{}".format(idx+1)
        else:
            prefix = "wikidata"
        ret["{}Id".format(prefix)] = item["id"]
        ret["{}Name".format(prefix)] = item.get("label","")
        ret["{}Description".format(prefix)] = item.get("description","")
        ret["{}Url".format(prefix)] = item["concepturi"]
    return ret

def wikify2(phrase, description=None):
    #wikification
    ret = {}
    wikiterm = wikipedia.search(phrase)
    for idx, term in enumerate(wikiterm[0:MAX_RESULT]):
        wikipage = wikipedia.page(term)
        ret["wikipedia_{}_url".format(idx)] = wikipage.url
        ret["wikipedia_{}_desc".format(idx)] = wikipedia.summary(term, sentences=1)

    return ret

def wikify3(phrase, description=None):
    ret = {}
    urlBase = "https://en.wikipedia.org/w/api.php?action=opensearch&format=json&formatversion=2&search={}&namespace=0&limit=10&suggest=true"
    url = urlBase.format(re.sub("\s+","%20",phrase))
    r = requests.get(url)
    jsonData = json.loads(r.content)
    #logging.info(items)
    ret = {}
    for idx, label in enumerate(jsonData[1][0:MAX_RESULT]):
        description = jsonData[2][idx]
        url = jsonData[3][idx]
        #if "refer to:" in description:
        #    continue

        if idx > 0:
            prefix = "wikipedia{}".format(idx+1)
        else:
            prefix = "wikipedia"
        ret["{}Label".format(prefix)] = label
        ret["{}Description".format(prefix)] = description
        ret["{}Url".format(prefix)] = url
    return ret

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)

    optional_params = {
        '--phrase': 'phrase'
    }
    main_subtask(__name__, optional_params=optional_params)

"""
    python wikify.py task_wikify --phrase="birth place"

"""
