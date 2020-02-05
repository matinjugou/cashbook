import os
import configparser

conf = configparser.ConfigParser()
conf.read('config.ini')
database_address = conf.get('App', 'DATABASE_ADDRESS')

debug = False
if conf.get('App', 'DEBUG') == 'TRUE':
    debug = True
