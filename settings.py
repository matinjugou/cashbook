import os
import configparser

conf = configparser.ConfigParser()
conf.read('config.ini')
database_address = conf.get('App', 'DATABASE_ADDRESS')
password = conf.get('App', 'PASSWORD')
jwt_secret = conf.get('App', 'JWT_SECRET')

debug = False
if conf.get('App', 'DEBUG') == 'TRUE':
    debug = True
