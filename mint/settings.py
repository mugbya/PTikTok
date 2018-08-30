import os

PACKAGE_NAME = os.path.basename(os.getcwd())


STATIC_URL = 'webContent/static'
MEDIA_URL = '/root/PTokTikTask/crawler'
# MEDIA_URL = '/Users/mugbya'
TEMPLATES = "webContent/templates"

REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_DB = '0'
REDIS_PASSWORD = ''

SPIDER_NAME = 'toktik'

HOST = '0.0.0.0'
PORT = 8000



