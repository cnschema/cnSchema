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

from cdata.table import json2excel, excel2json
from cdata.core import stat, json_get_list, any2utf8, file2abspath, file2json,json2file
from cdata.misc import main_subtask

from schemaorg import Schemaorg

try:
     # Python 2.6-2.7
     from HTMLParser import HTMLParser
except ImportError:
     # Python 3
     from html.parser import HTMLParser

h = HTMLParser()
def clean_schemaorg_description(text):
    temp = text
    temp = re.sub(ur"\n", " ", temp)
    #temp = re.sub(ur"Related .*$", "", temp)
    #temp = re.sub(ur"<ul.+$", "", temp)
    temp = re.sub(ur"<[^>]+>", "", temp)
    temp = re.sub(ur"\s+", " ", temp)
    #temp = re.sub("\n.*", "", temp)
    #temp = re.sub("\..+", ".", temp).strip()

    temp = h.unescape(temp)

    if not temp:
        logging.warning( temp )
    elif temp != text:
        logging.warning( text )
        logging.warning( temp )
    return temp

def split_string_by_comma(text):
    text = text.strip()
    ret = [x.strip() for x in re.split(ur"[,，、]", text) if x.strip()]
    return ret

####################################################

def read_cns_core(version):
    name = "cns-core"
    filename = "../local/releases/{}/{}.xls".format(version, name)
    filename = file2abspath(filename, __file__)


    temp = excel2json(filename)
    keys = temp["fields"].values()[0]
    items = temp["data"].values()[0]
    logging.info(len(items))

    #cleanup
    itemsNew = []
    for item in items:
        itemNew = {}
        for p in item.keys():
            #skip commented fields
            if p.startswith("#"):
                continue

            itemNew[p] = item.get(p,"")

            if p == "description":
                itemNew[p] = clean_schemaorg_description(itemNew[p])
            #if p == "@id":
            #    itemNew["schemaorgUrl"] = itemNew[p]
            #    itemNew[p] = re.sub("http://schema.org", "http://cnschema.org", itemNew[p])
        itemsNew.append(itemNew)
    items = itemsNew
    #keys = [x for x in keys if x in items[0].keys()]

    return items

def write_cns_core(items, version):
    name = "cns-core"

    # write excel
    keys = [
        "category",
        "@id",
        "name",
        "description",
        "supersededBy",
        "nameZh",
        "descriptionZh",
        "alternateName",
        "wikidataName",
        "wikidataUrl",
        "wikipediaUrl",
        "schemaorgUrl"
    ]

    for key in keys:
        assert key in items[0].keys()

    filename = "../data/releases/{}/{}.xls".format(version, name)
    filename = file2abspath(filename, __file__)
    #json2excel(items, keys, filename)


    # write json-ld
    for item in items:
        p = "alternateName"
        item[p] = split_string_by_comma(item.get(p,""))

    filename = "../data/releases/{}/{}.jsonld".format(version, name)
    filename = file2abspath(filename, __file__)
    with codecs.open(filename,"w",encoding="utf-8") as f:
        output = {
          "@context": {
#            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
#            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "@vocab": "http://cnschema.org/"
          },
          "@graph": items
         }

        json.dump(output, f, ensure_ascii=False, sort_keys=True, indent=4)


def task_cns_json2excel(args=None):
    name = "cns-core"
    version = "3.2"

    filename = "../data/releases/{}/{}.jsonld".format(version, name)
    filename = file2abspath(filename, __file__)
    items = file2json(filename)["@graph"]

    logging.info(items)

    filename = "../data/releases/{}/{}.xls".format(version, name)
    filename = file2abspath(filename, __file__)
    #json2excel(items, fileds, filename)

def task_cns_rebuild(args=None):
    name = "cns-core"
    version = "3.2"

    filename = "../data/releases/{}/{}.xls".format(version, name)
    filename = file2abspath(filename, __file__)
    temp = excel2json(filename)
    keys = temp["fields"].values()[0]
    items = temp["data"].values()[0]

    #logging.info(items)

    write_cns_core(items, version)


def task_cns_core(args=None):
    name = "cns-core"
    version = "3.2"

    items = read_cns_core(version)
    so = Schemaorg(version)
    map_id_schemaorg = so.load_data()

    # for item in map_id_schemaorg.values():
    #     if item["_group"] == "other":
    #         logging.info(item["@id"])
    # exit()

    for item in items:
        schemaorg_id = item["schemaorgUrl"]
        supersede_id = map_id_schemaorg[schemaorg_id].get("http://schema.org/supersededBy",{}).get("@id","")
        if supersede_id:
            logging.info(supersede_id)
        item["supersededBy"]= supersede_id

    write_cns_core(items, version)


if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)

    main_subtask(__name__)

"""
    python cns.py task_cns_core

    python cns.py task_cns_json2excel

    python cns.py task_cns_rebuild

"""
