import MySQLdb as mdb
import json
import datetime
from peewee import *
from constants import *
import pandas as pd

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.price import Price
from boto.mturk.qualification import *

ACCESS_ID = 'AMT_ACCESS_ID'
SECRET_KEY = 'AMT_SECRET_KEY'
HOST = 'mechanicalturk.amazonaws.com'
SANDBOX_HOST = 'mechanicalturk.sandbox.amazonaws.com'
mtc = None
is_prod = False

def getConnection(is_prod = True):
    if is_prod:
        mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=HOST)
    else:
        mtc = MTurkConnection(aws_access_key_id=ACCESS_ID,
                      aws_secret_access_key=SECRET_KEY,
                      host=SANDBOX_HOST)



    print mtc.get_account_balance()
    return mtc

def price(amount):
    return Price(amount=amount, currency_code='USD')

config = json.load(open('config.json', 'r'))

import sys
sys.path.append(config['root'])
from createDatabase import *

con = mdb.connect(host="localhost", user=config['db_user'], db=config['db_name'], passwd=config['db_pass'])
db = MySQLDatabase(config['db_name'], user=config['db_user'], password=config['db_pass'])

def payForHits(is_prod = False):
    mtc = getConnection(is_prod)

    payQHits = AMTHits.select(AMTHits.assignmentId, AMTHits.socketId, AMTHits.workerId, AMTHits.approve, AMTHits.status, AMTHits.isPaid)\
               .where((AMTHits.approve != 'notApprove') & (AMTHits.isPaid == 0) & (AMTHits.status == 'finished'))
               # .where(AMTHits.approve == 'approve')
    count = 0
    for q in payQHits:
        # print(q.approve)
        try:
            if q.approve == 'approve':
                print 'Paying for ', q.assignmentId, q.workerId, q.socketId
                mtc.approve_assignment(q.assignmentId)
                updateAMTHits = AMTHits.update(isPaid = 1)\
                            .where((AMTHits.assignmentId == q.assignmentId) & (AMTHits.socketId == q.socketId) & (AMTHits.workerId == q.workerId))
                updateAMTHits.execute()
                count += 1
            elif q.approve == 'reject':
                print 'Rejecting ', q.assignmentId, q.workerId, q.socketId
                feedback = 'Please keep your responses conversational and relevant to the image, and refrain from using chat/IM language. Thanks for contributing!'
                mtc.reject_assignment(q.assignmentId, feedback=feedback)
                updateAMTHits = AMTHits.update(isPaid = 1)\
                            .where((AMTHits.assignmentId == q.assignmentId) & (AMTHits.socketId == q.socketId) & (AMTHits.workerId == q.workerId))
                updateAMTHits.execute()
                count += 1
        except:
            print 'Already paid or wrong is_prod.'

    print 'Count: ', count


payForHits(True)

