# -*- coding: utf-8 -*-
# author: Li Ding


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
import copy

from cdata.core import json_get_list, file2abspath, json2file, file2json, stat
from cdata.misc import main_subtask

import requests
import requests_cache

PLIST_BASIC = ["@id","rdfs:label","rdfs:comment", "_supersede", "_usage", "_layer","_examples","_instances"]
PLIST_REF = ["@id","rdfs:label"]
PLIST_DOMAIN_RANGE = [
    "http://schema.org/rangeIncludes",
    "http://schema.org/domainIncludes"]

INVERSE_DOMAIN_RANGE = {
    "http://schema.org/domainIncludes":"isDomainOf",
    "http://schema.org/rangeIncludes":"isRangeOf"}

PLIST_OBJ = [
    "http://schema.org/inverseOf",
    "http://schema.org/supersededBy"]

PLIST_PROP = PLIST_BASIC + PLIST_DOMAIN_RANGE + INVERSE_DOMAIN_RANGE.values() + PLIST_OBJ


def json_append(obj, p, v):
    vlist = obj.get(p,[])
    if vlist:
        vlist.append(v)
    else:
        obj[p] = [v]

def get_usage_str(usage_id):
    if (usage_id == '1') :
        return "Between 10 and 100 domains"
    elif (usage_id == '2'):
        return "Between 100 and 1000 domains"
    elif (usage_id == '3'):
        return "Between 1000 and 10,000 domains"
    elif (usage_id == '4'):
        return "Between 10,000 and 50,000 domains"
    elif (usage_id == '5'):
        return "Between 50,000 and 100,000 domains"
    elif (usage_id == '7'):
        return "Between 100,000 and 250,000 domains"
    elif (usage_id == '8'):
        return "Between 250,000 and 500,000 domains"
    elif (usage_id == '9'):
        return "Between 500,000 and 1,000,000 domains"
    elif (usage_id == '10'):
        return "Over 1,000,000 domains"
    else:
        return ""


def load_examples(lines):
    examples = []
    for line in lines:
        #line = line
        if not line.strip():
            continue

        if line.startswith("TYPES:"):
            types = [x.strip() for x in re.split("[\s,]+",line[6:]) if x.strip() and not x.startswith("#")]
            state = "TYPES"
            example = collections.defaultdict(list)
            example[state] = types
            examples.append(example)
        elif line in ["PRE-MARKUP:", "MICRODATA:", "RDFA:","JSON:"]:
            state = line[:-1]
        else:
            example[state].append(line.decode("utf-8"))

    for example in examples:
        for p in ["PRE-MARKUP", "MICRODATA", "RDFA","JSON"]:
            example[p] = u"\n".join(example[p])

        p = "PRE-MARKUP"
        example[p] = re.sub(ur"&amp;", "&", example[p])

    logging.info(len(examples))
    return examples


class Schemaorg:
    def __init__(self, version):
        self.version = version
        self.url_base = "https://raw.githubusercontent.com/schemaorg/schemaorg/master"
        self.dir_output = "../local/releases/{}".format(version)
        self.dir_output = file2abspath(self.dir_output, __file__)


    def load_data(self):
        filename_cache = os.path.join(self.dir_output, "schemaorg.json")
        if os.path.exists(filename_cache):
            return file2json(filename_cache)
        elif not os.path.exists(os.path.dirname(filename_cache)):
            os.makedirs(os.path.dirname(filename_cache))

        #examples
        self._init_examples()

        # the word count stats 2015
        self._init_stat2015()

        # init the schema, with information from examples and stats
        self._init_schema()

        json2file(self.map_id_node, filename_cache)

        return self.map_id_node


    def _copy_node(self, v, plist=PLIST_BASIC, simplify=False):
        ret = {}
        for p in plist:
            if not p in v:
                continue

            if simplify:
                pX = os.path.basename(p)
            else:
                pX = p

            if p in PLIST_DOMAIN_RANGE:
                ret[pX] = []
                for rX in json_get_list(v, p):
                    r = self.map_id_node.get(rX["@id"])
                    ret[pX].append(self._copy_node(r, PLIST_REF))
                if ret[pX]:
                    ret[pX][-1]["_last"] = True
            elif p in PLIST_OBJ:
                r = self.map_id_node.get(v[p]["@id"])
                ret[pX] = self._copy_node(r, PLIST_REF)
            else:
                ret[pX] = v[p]


        #logging.info(ret.keys())
        return ret

    def _init_examples(self):
        self.map_id_examples = collections.defaultdict(list)

        url = "https://github.com/schemaorg/schemaorg/tree/master/data"
        r = requests.get(url)
        logging.info(r.content)
        filenames = re.findall(r"data/[\w\-]*examples.txt", r.content)

        url_base = "https://github.com/schemaorg/schemaorg/raw/master"
        urls =  [ url_base+"/"+x for x in filenames]

        for url in urls:
            logging.info(url)
            examples = load_examples(re.split("\n",requests.get(url).content))
            for example in examples:
                example["_source"] = url
                #logging.info(example)
                for xtype in example["TYPES"]:
                    x = copy.deepcopy(example)
                    x["_index"] = len(self.map_id_examples[xtype])+1
                    self.map_id_examples[xtype].append(x)

    def _init_stat2015(self):
        self.map_id_stat2015 = {}
        filename = "2015-04-vocab_counts.txt"
        url = '{}/data/{}'.format(self.url_base,  filename)
        r = requests.get(url)

        for idx, line in enumerate(re.split("\n",r.content)):
            #line =line.strip()
            if not line:
                continue
            temp = re.split("\t",line)
            if len(temp) != 2:
                logging.warn("bad input at line {}, [{}]".format(idx, line))
                continue
            name, usage_id = temp
            self.map_id_stat2015[name] = usage_id

    def _init_schema(self):
        # the main json-ld
        self.map_id_node = {}
        filename = "schema.jsonld"
        url = '{}/data/releases/{}/{}'.format(self.url_base, self.version, filename)
        #logging.info(url)
        r = requests.get(url)
        data_jsonld = json.loads(r.content)
        logging.info(len(data_jsonld))

        for node in data_jsonld["@graph"]:
            if "schema.org" not in node["@id"]:
                logging.debug(node["@id"])
                # node.get("@type")
                pass

            type_list = node.get("@type",[])
            if not type(type_list) == list:
                type_list = [type_list]
            else:
                node["@type"] = sorted(type_list)
            node["xtype"] = ','.join(type_list)


        #first pass
        for node in data_jsonld["@graph"]:
            xid = node["@id"]
            self.map_id_node[xid] = node

            #group
            xtypeList = json_get_list(node, "@type")
            if "rdfs:Class" in xtypeList:
                node["_group"] = "type"
            elif "rdf:Property" in xtypeList:
                node["_group"] = "property"
            else:
                node["_group"] = "other"

            node["_layer"] = "core"

            #nameCount
            usage_id = self.map_id_stat2015.get(node.get("rdfs:label"))
            node["_usage"] = get_usage_str(usage_id)

            examples = self.map_id_examples.get(node.get("rdfs:label"))
            if examples:
                node["_examples"] = examples

        #second pass
        for node in data_jsonld["@graph"]:
            xid = node["@id"]

            # instances
            for xtype in json_get_list(node, "@type"):
                the_node = self.map_id_node.get(xtype)
                if the_node:
                    json_append(the_node, "_instances", self._copy_node(node, PLIST_REF))
                    the_node["_instances"] = sorted(the_node["_instances"], key=lambda x:x["rdfs:label"])
            # subclass relation
            for p in ["rdfs:subClassOf", "rdfs:subPropertyOf"]:
                for v in json_get_list(node, p):
                    node_id = v["@id"]
                    if node_id not in self.map_id_node:
                        continue

                    the_node = self.map_id_node[node_id]
                    json_append(node, "_super", node_id)
                    json_append(the_node, "_sub", xid)

            #domain range
            if node["_group"]  == "property":
                for p in PLIST_DOMAIN_RANGE:
                    for the_node in json_get_list(node, p):
                        refxid = the_node["@id"]
                        pX = INVERSE_DOMAIN_RANGE[p]
                        json_append(self.map_id_node[refxid], pX, node)
                        self.map_id_node[refxid][pX]= sorted(self.map_id_node[refxid][pX], key=lambda x:x["rdfs:label"])

            # http://schema.org/supersededBy
            p = "http://schema.org/supersededBy"
            if p in node:
                node_id = node[p]["@id"]
                the_node = self.map_id_node[node_id]
                the_node["_supersede"] = self._copy_node(node, PLIST_REF)
                #logging.info(the_node)
                #exit()

def task_init(args=None):
    so = Schemaorg("3.4")
    data = so.load_data()
    stat(data.values(),[], ["_group","@type"])
    logging.info(len(data))


def task_superclasses(args):
    filename = "../local/releases/3.4/schema_taxonomy.json"
    filename = file2abspath(filename, __file__)
    data = file2json(filename)
    pairs = []
    loadmapping(data, [], pairs)
    logging.info(json.dumps(pairs, indent=4, ensure_ascii=False))

    mapping = collections.defaultdict(list)
    for pair in pairs:
        key = pair["to"]
        mapping[key].append(pair["to"])

    for pair in pairs:
        key = pair["to"]
        for parent in pair["path"]:
            if parent not in mapping[key]:
                mapping[key].append(parent)

    logging.info(json.dumps(mapping, indent=4, ensure_ascii=False))
    filename = "../data/releases/3.4/schema.superclass.json"
    filename = file2abspath(filename, __file__)
    json2file(mapping, filename)


def loadmapping(node, path, pairs):
    for child in node.get("children", []):
        path_child = []
        path_child.extend(path)
        path_child.append(node["name"])
        pairs.append({"form": node["name"], "to": child["name"],
                      "path": path_child})
        loadmapping(child, path_child, pairs)


if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.INFO)  # noqa
    logging.getLogger("requests").setLevel(logging.WARNING)

    filename = '../local/cache'
    filename = file2abspath(filename, __file__)
    requests_cache.install_cache(filename)

    main_subtask(__name__)

"""
    python schemaorg.py task_init
    python schemaorg.py task_superclasses
"""
