import MySQLdb as mdb
import datetime
import sys
import os
from peewee import *
import glob
from collections import defaultdict
import json
import shortuuid
import random
from createDatabase import *

config = json.load(open('config.json', 'r'))
con = mdb.connect(host="localhost", user=config['db_user'], db=config['db_name'], passwd=config['db_pass'])
database = MySQLDatabase(config['db_name'], user=config['db_user'], password=config['db_pass'])

# This creates db tables if they don't exist
createDatabaseTables()

# This populates the 'image' and 'caption' tables with all images from train2014 and one randomly chosen caption per image
# TODO:
# 1) Create a symbolic link from `static/dataset` to `/path/to/mscoco/images/`
# 2) Create folder `static/annotations` and download COCO caption files (captions_train2014.json, etc)
# fillPilotData()

# This pushes 3000 images from the 'image' table with numHitsFinished == 0 to the redis queue 'visdial_queue'
# createRedisQueue()

