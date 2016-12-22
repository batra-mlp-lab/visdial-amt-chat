import redis
from peewee import *
from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
import sys

r = redis.StrictRedis(host='localhost', port=6380, db=0, password = 'REDIS_PASSWORD_HERE') # TODO

ACCESS_ID = 'AMT_ACCESS_ID' # TODO
SECRET_KEY = 'AMT_SECRET_KEY' # TODO
HOST = 'mechanicalturk.sandbox.amazonaws.com'

mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)

url = "https://ENTER_HIT_URL/" # TODO
title = "Live Q/A about an Image (With Captions)"
description = "Ask or Answer questions about an image with a fellow Turker."
keywords = ["image", "chat", "question", "answer"]
frame_height = "1200"
amount = 0.15

form = ExternalQuestion(url, frame_height)

QUES_HITS_FILE = 'amthitsQues.csv'
ANS_HITS_FILE = 'amthitsAns.csv'
QUES_REJECTS_FILE = 'amthitsReviewRejectQues.csv'
ANS_REJECTS_FILE = 'amthitsReviewRejectAns.csv'

