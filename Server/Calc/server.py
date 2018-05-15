import time
import sys
import cherrypy
import os

from paste.translogger import TransLogger
from app import create_app
from pyspark import SparkContext, SparkConf

def init_spark_context():
    # load spark context
    conf = SparkConf().setAppName("book_recommendation-server")
    # IMPORTANT: pass aditional Python modules to each worker
    sc = SparkContext(conf=conf, pyFiles=['engine.py', 'app.py'])
 
    return sc
 

def run_server(app):
 
    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)
 
    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')
    # cherrypy_cors.install()
    
    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 5432,
        'server.socket_host': '0.0.0.0'
        # 'tools.CORS.on': True,
        # 'cors.expose.on': True,
        # 'tools.response_headers.on': True,
        # 'tools.response_headers.headers': [('Access-Control-Allow-Origin', '*'), ("Access-Control-Allow-Methods", "GET, POST, HEAD, PUT, DELETE"), ("Access-Control-Max-Age","1782000")]
    })
    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    
    cherrypy.engine.block()
 
 
if __name__ == "__main__":
    # Init spark context and load libraries
    # sc = init_spark_context()
    sc=None
    #  dataset_path = os.path.join('../Data', 'BX-CSV-Dump')
    # dataset_path = os.path.join('../Data')
    dataset_path = os.path.abspath(os.path.join(os.getcwd(), '../Data'))
    app = create_app(sc, dataset_path)
    # start web server
    run_server(app)

