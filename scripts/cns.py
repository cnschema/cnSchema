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
from cdata.core import stat, json_get_list, any2utf8, file2abspath, file2json,json2file, json_dict_copy
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


def json_append(obj, p, v):
    vlist = obj.get(p,[])
    if vlist:
        vlist.append(v)
    else:
        obj[p] = [v]

def create_dir_if_not_exist(filename):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

####################################################

def read_cns_core_excel(version, path="local"):
    name = "cns-core"
    filename = "../{}/releases/{}/{}.xls".format(path, version, name)
    filename = file2abspath(filename, __file__)

    temp = excel2json(filename)
    keys = temp["fields"].values()[0]
    items = temp["data"].values()[0]
    logging.info(len(items))

    return items

def read_cns_core_jsonld(version, path="data"):
    name = "cns-core"
    filename = "../{}/releases/{}/{}.jsonld".format(path, version, name)
    filename = file2abspath(filename, __file__)
    items = file2json(filename)["@graph"]

    return items



def rewrite_cns_core(items):
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

    # add supersede relation
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

    return items


def write_cns_core(items, version, formats=["excel","jsonld"]):
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

    # validation
    for key in keys:
        assert key in items[0].keys()

    # write excel
    if "excel" in formats:
        filename = "../data/releases/{}/{}.xls".format(version, name)
        filename = file2abspath(filename, __file__)
        json2excel(items, keys, filename)


    # write json-ld
    if "jsonld" in formats:
        for item in items:
            p = "alternateName"
            item[p] = split_string_by_comma(item.get(p,""))

        filename = "../data/releases/{}/{}.jsonld".format(version, name)
        filename = file2abspath(filename, __file__)
        output = {
          "@context": {
            "@vocab": "http://cnschema.org/"
          },
          "@graph": items
         }
        json2file(filename, output)


def dup(items, prop, threshold=1):
    counter = collections.Counter()
    for item in items:
        counter[item.get(prop,"")]+=1
    for key, cnt in counter.most_common():
        if cnt <= threshold:
            continue
        print key, cnt

def task_cns_core_init(args=None):
    name = "cns-core"
    version = "3.2"

    items = read_cns_core_excel(version, path="local")
    items = rewrite_cns_core(items)

    write_cns_core(items, version, formats=["excel","jsonld"])

def task_cns_core_excel2json(args=None):
    name = "cns-core"
    version = "3.2"

    items = read_cns_core_excel(version, path="data")

    #logging.info(items)
    stat(items, ["wikidataUrl","wikidataName","wikipediaUrl","nameZh","descriptionZh"])
    dup(items, "wikidataName")
    dup(items, "wikidataUrl")
    dup(items, "wikipediaUrl")

    write_cns_core(items, version, formats=["jsonld"])

def task_cns_core_json2excel(args=None):
    name = "cns-core"
    version = "3.2"

    items = read_cns_core_jsonld(version, path="data")
    #logging.info(items)

    write_cns_core(items, version, formats=["excel"])


####################################################
def schemaorg2cnschema(data):
    temp_text = json.dumps(data, ensure_ascii=False)
    temp_text = re.sub("schema.org","cnschema.org", temp_text)
    return json.loads(temp_text)



PLIST_CNSCHEMA = ["nameZh","descriptionZh","wikidataUrl", "wikidataName","wikipediaUrl"]
PLIST_BASIC = ["@id","rdfs:label","rdfs:comment", "_supersede", "_usage", "_layer","_examples","_instances"] + PLIST_CNSCHEMA
PLIST_REF = ["@id","rdfs:label"]
PLIST_DOMAIN_RANGE = ["http://cnschema.org/rangeIncludes","http://cnschema.org/domainIncludes"]
INVERSE_DOMAIN_RANGE ={
"http://cnschema.org/domainIncludes":"isDomainOf",
"http://cnschema.org/rangeIncludes":"isRangeOf",
}
PLIST_OBJ = ["http://cnschema.org/inverseOf", "http://cnschema.org/supersededBy"]
PLIST_PROP = PLIST_BASIC + PLIST_DOMAIN_RANGE + INVERSE_DOMAIN_RANGE.values() + PLIST_OBJ


class WebsiteV1():
    def __init__(self, version, site, map_id_schemaorg):
        self.version = version
        self.site = site
        self.dir_output = os.path.join(os.path.dirname(__file__), "../local/releases/{}/").format(self.version)
        self.map_id_schemaorg = map_id_schemaorg

    def run(self):
        self.download_page_docs()
        self.generate_page_entity_detail()

    def download_page_docs(self):

        # from github
        #url = "https://github.com/schemaorg/schemaorg/tree/master/docs"
        url = "https://github.com/cnschema/cnschema/tree/master/docs"
        r = requests.get(url)
        logging.info(r.content)
        filenames = re.findall(r"(docs/[^\"]+\.(css|js))", r.content)

        #urlBase = "https://github.com/schemaorg/schemaorg/raw/master"
        urlBase = "https://github.com/cnschema/cnschema/raw/master"
        for fx in filenames:
            filename = fx[0]

            url = urlBase + "/" + filename
            logging.info(url)
            r = requests.get(url)

            # logging.info(filename)
            filename = os.path.join(self.dir_output, "{}/".format(self.site), filename)
            create_dir_if_not_exist(filename)
            with codecs.open(filename,'wb') as f:
                content = r.content
                f.write( content )


    def generate_page_entity_detail(self):
        # write html using template file
        filename = os.path.join(os.path.dirname(__file__), "../templates/page.mustache")
        with codecs.open (filename, encoding="utf-8") as f:
            templatePage = f.read()

        import pystache

        for xid in sorted(self.map_id_schemaorg):
            item = self.map_id_schemaorg.get(xid)

            if "#" in xid:
                logging.warn("skip {}".format(xid))
                continue

            entry = self.convert_extend2mustach( item )

            html = pystache.render(templatePage, entry)
            filename = os.path.join(self.dir_output, "{}/{}.html".format(self.site, entry["rdfs:label"]))
            create_dir_if_not_exist(filename)
            with codecs.open(filename, "w", encoding="utf-8") as f:
                f.write(html)

            #filename = os.path.join(self.dir_output, "{}/{}.json".format(self.site, entry["rdfs:label"]))
            #json2file( entry, filename)

            #print html

    def _gen_path(self, p, node, path, result):
        if p in node:
            for v in node[p]:
                nextNode = self.map_id_schemaorg[v]
                self._gen_path( p, nextNode, path + [nextNode], result)
        else:
            temp = []
            for node in reversed(path):
                temp.append(self._copy_data( node, PLIST_REF))
            temp[-1]["_lastone"] = True
            result.append({"_path":temp})


    def _copy_data(self, v, plist=PLIST_BASIC, simplify=False):
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
                    r = self.map_id_schemaorg.get(rX["@id"])
                    ret[pX].append(self._copy_data( r, PLIST_REF))
                if ret[pX]:
                    ret[pX][-1]["_last"] = True
            elif p in PLIST_OBJ:
                r = self.map_id_schemaorg.get(v[p]["@id"])
                ret[pX] = self._copy_data( r, PLIST_REF)
            else:
                ret[pX] = v[p]

        #logging.info(ret.keys())
        return ret

    def convert_extend2mustach(self, node):
        xid = node["@id"]
        entry = self._copy_data( node, PLIST_PROP, simplify=True)

        entry["_node_label"] = node["rdfs:label"]
        entry["_group_{}".format(node["_group"])] = True

        #source
        p = "http://purl.org/dc/terms/source"
        sourceList = json_get_list(node, p)
        for sourceRef in sourceList:
            if not type(sourceRef) == dict:
                logging.error(sourceList)
                continue

            #logging.info(node[p])
            source = self.map_id_schemaorg.get(sourceRef["@id"])
            if source:
                temp = source
                json_append(entry, "_sourceAck", temp)
            else:
                temp = {}
                temp["@id"] = sourceRef["@id"]
                temp["rdfs:label"] = sourceRef["@id"]
                temp["rdfs:comment"] = '<a href="{}">{}</a>'.format(sourceRef["@id"],sourceRef["@id"])
                json_append(entry, "_source", temp)

        if node["_group"] == "property":
            result = []
            self._gen_path( "_super", node, [node], result)

            rootPath = [ self._copy_data( self.map_id_schemaorg["http://cnschema.org/Thing"], PLIST_REF),
                                {"rdfs:label":"Property", "@id":"http://meta.cnschema.org/Property"}]
            entry["_paths"] = []
            for onePath in result:
                temp = []
                temp.extend(rootPath)
                temp.extend(onePath["_path"])
                temp[-1]["_lastone"] = True
                entry["_paths"].append({"_path":temp})

        if node["_group"] == "other":
            result = []
            typeNode = self.map_id_schemaorg.get(node["@type"])
            self._gen_path( "_super", typeNode, [typeNode], result)
            entry["_paths"] = result
            entry["_is_instance"] = True

        if node["_group"] == "type":
            #path
            result = []
            self._gen_path( "_super", node, [node], result)
            #logging.info(result)
            entry["_paths"] = result

            #domain
            p = "http://cnschema.org/domainIncludes"
            p = "isDomainOf"
            pX = os.path.basename(p)
            entry["_pTree"]=[]
            seedList = [xid]
            while seedList:
                newSeedList = []
                for seedId in seedList:
                    seed = self.map_id_schemaorg.get(seedId)

                    treeItem = self._copy_data( seed)
                    treeItem["_properties"] = []

                    for v in sorted(seed.get(p,[]), key=lambda x:x["@id"]):
                        if "http://cnschema.org/supersededBy" in v:
                            continue


                        prop = self._copy_data( v, plist=PLIST_PROP, simplify=True)

                        # if v["@id"] == "http://cnschema.org/offeredBy":
                        #     logging.info(v.keys())
                        #     logging.info(prop.keys())
                        #     exit()

                        #logging.info(prop)
                        #exit()
                        treeItem["_properties"].append(prop)
                        #break #TODO

                    if treeItem["_properties"]:
                        entry["_pTree"].append(treeItem)

                    newSeedList.extend( seed.get("_super",[]) )
                    #logging.info(v)
                seedList = newSeedList
            if entry["_pTree"]:
                entry["_pTree"][-1]["_last"]=True

            #range
            p = "http://cnschema.org/rangeIncludes"
            p = "isRangeOf"
            pX = "_pRange"
            if node.get(p,[]):
                entry[pX]=[]
                for v in sorted(node.get(p,[]), key= lambda x:x["@id"]):
                    prop = self._copy_data( v,plist=PLIST_PROP, simplify=True)
                    entry[pX].append(prop)


        #super and sub
        for p in ["_sub", "_super"]:
            if node.get(p, []):
                entry[p] = []
                for v in node.get(p, []):
                    relNode = self.map_id_schemaorg.get(v)
                    entry[p].append(self._copy_data( relNode, PLIST_REF))

        entry["_sitename"] = self.site #"schema.org" # self.site

        entry["_version"] = self.version
        entry["_url_root"] = "."
        entry["_url_schema"] = "http://{}".format(self.site) # "http://schema.org"

        #entry["_examples"] = []
        for k, v in entry.items():
            if type(v) == list  and v and type(v[0]) in [dict,collections.defaultdict]:
                v[-1]["_last"] = True
            #logging.info(k)
            #logging.info(type(v))
            #logging.info(type(v[0]))
        #exit()

        return entry



MAP_CNSCHEMA = [ {"name":x} for x in PLIST_CNSCHEMA]



def task_cns_make_html(args=None):
    name = "cns-core"
    version = "3.2"
    site = "cnschema.org"

    items = read_cns_core_jsonld(version, path="data")
    map_id_cnschema = {}
    for item in items:
        schemaorg_id = item["schemaorgUrl"]
        map_id_cnschema[schemaorg_id] = item

    # update map_id_schemaorg with cnschem properties
    so = Schemaorg(version)
    map_id_schemaorg = so.load_data()
    for entry in map_id_schemaorg.values():
        entry.update(json_dict_copy(map_id_cnschema.get(entry["@id"],{}), MAP_CNSCHEMA))
        for p in ["isDomainOf","isRangeOf"]:
            target_list = entry.get(p,[])
            for target in target_list:
                target.update(json_dict_copy(map_id_cnschema.get(target["@id"],{}), MAP_CNSCHEMA))


    #rewrite map_id_schemaorg schema.org => cnschema.org    items_new = schemaorg2cnschema(items_new)
    map_id_schemaorg = schemaorg2cnschema(map_id_schemaorg)

    filename = '../local/releases/3.2/cns-core.extend.json'
    filename = file2abspath(filename, __file__)
    json2file(map_id_schemaorg ,filename)

    website = WebsiteV1(version, site, map_id_schemaorg)
    website.run()


def task_cns_template(args=None):
    mapping = {
        "version":[u"版本"],
        "domain":[u"直属分类"],
        "name":[u"规范属性名"],
        "nameZh":[u"cnschema属性名"],
        "alternateName":[u"中文属性名"],
        "nameSchemaorg":[u"schema.org属性名"],
        "nameWikidata":[u"wikidata属性名"],
        "descriptionWikipedia":[u"wikipedia定义"],
        "range":[u"预期的属性类型"],
        "value":[u"example value"],
        "jsonld":[u"example json-ld"],
    }

    filename = "../local/201707/cns-t-organization.xls"
    filename = file2abspath(filename, __file__)
    excel_data = excel2json(filename)
    bindings = collections.defaultdict(dict)
    for sheet_data in excel_data["data"].values():
        if len(sheet_data) == 0:
            continue
        logging.info(len(sheet_data))
        for row in sheet_data:
            logging.info(json.dumps(row, ensure_ascii=False))
            domain = row["domain"] #row[u"直属分类"]
            propName = row[u"name"]
            rangeList = row[u"range"]
            bindings[domain][propName] = row

        break

    logging.info(bindings)

if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)

    main_subtask(__name__)

"""
    python cns.py task_cns_core_init

    python cns.py task_cns_core_excel2json

    python cns.py task_cns_core_json2excel

    python cns.py task_cns_make_html

    python cns.py task_cns_template

"""
