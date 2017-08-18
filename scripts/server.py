# -*- coding: utf-8 -*-
'''



'''


import datetime
import logging
import urllib
import sys
import os
import time
import json
import traceback
import argparse

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import bottle
from bottle import route, run, request, get, post, response
from elasticsearch import Elasticsearch

from cdata.misc import main_subtask
from cdata.core import file2abspath, any2unicode, file2json
from search import CnsSearch

@get('/debug/version')
def version():
    msg = {"ok": True, "version":"0.2.0.20170805", "since": START_TIME}  #
    return msg


# http://stackoverflow.com/questions/17262170/bottle-py-enabling-cors-for-jquery-ajax-requests
# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors


app = bottle.app()
cns = CnsSearch()


#http://106.75.79.180:9200/hbrain_market_price_v2.0/predict/search?pretty&filter_path=took,hits.total,hits.hits.source
@app.route('/autocomplete', method=['GET'])
@enable_cors
def autocomplete():
    #logging.info(request)
    try:
        q = request.query.get("q")
        return cns.es_autocomplete(q)
    except:
        traceback.print_exc()
        logging.info("error")
        return ""



@enable_cors
@app.route('/search', method=['GET'])
def search():
    try:
        q = request.query.get("q")
        offset = request.query.get("offset", 0)
        return cns.es_search(q, offset)
    except:
        traceback.print_exc()
        logging.info("error")
        return ""



def start():
    #http://stackoverflow.com/questions/13760109/ec2-bottle-py-connection
    app.run(host='0.0.0.0', port=18080)
    logging.info('completed %.3f' % time.clock())

def start2(number_of_process=4):
	from tornado.wsgi import WSGIContainer
	from tornado.httpserver import HTTPServer
	from tornado.ioloop import IOLoop

	http_server = HTTPServer(WSGIContainer(app))
	http_server.listen(18080)
	IOLoop.instance().start()

	logging.info('completed %.3f' % time.clock())


def task_server(args):
    global START_TIME
    START_TIME = datetime.datetime.now().isoformat()[0:19]
    logging.info( 'starting web service' )
    start2()


if __name__ == "__main__":
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)

    optional_params = {
        '--es_config_file': 'config'
    }
    main_subtask(__name__, optional_params=optional_params)


"""
    ####################
    ## run local server
    python server.py task_server

    ####################
    ## online release
    sh sync-up-server.sh


    ####################
    ## run elasticsearch server
    ~/cnschema.org/elasticsearch-5.5.2/bin/elasticsearch

    ####################
    ## run remote server
    ssh ....

    cd ~/cnschema/scripts/
    tmux

    python server.py task_server

    CTRL-b d
"""
