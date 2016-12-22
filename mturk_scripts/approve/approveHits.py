import json
import MySQLdb as mdb
import datetime
from peewee import *
from constants import *
import pandas as pd

config = json.load(open('config.json', 'r'))

import sys
sys.path.append(config['root'])
from createDatabase import *

con = mdb.connect(host="localhost", user=config['db_user'], db=config['db_name'], passwd=config['db_pass'])
db = MySQLDatabase(config['db_name'], user=config['db_user'], password=config['db_pass'])

def approveAllHits(file):

    hitsToApprove = pd.read_csv(file)
    approveHits = hitsToApprove.loc[hitsToApprove['approve'] == 'approve']
    uniqueApprove = approveHits.drop_duplicates(subset=['workerId', 'assignmentId', 'socketId'], keep = 'first')

    print(uniqueApprove)

    for index, row in uniqueApprove.iterrows():
        updateAMTHits = AMTHits.update(approve = 'approve')\
            .where((AMTHits.status == 'finished') & (AMTHits.approve == 'notApprove') & (AMTHits.assignmentId == str(row['assignmentId'])) & (AMTHits.socketId == str(row['socketId'])) & (AMTHits.workerId == str(row['workerId'])))
        updateAMTHits.execute()


    reviewReject = hitsToApprove.loc[hitsToApprove['approve'] == 'reviewReject']
    uniqueReviewReject = reviewReject.drop_duplicates(subset=['workerId', 'assignmentId', 'socketId'], keep = 'first')

    print(uniqueReviewReject)

    for index, row in uniqueReviewReject.iterrows():
        updateAMTHits = AMTHits.update(approve = 'reviewReject')\
            .where((AMTHits.status == 'finished') & (AMTHits.approve == 'notApprove') & (AMTHits.assignmentId == str(row['assignmentId'])) & (AMTHits.socketId == str(row['socketId'])) & (AMTHits.workerId == str(row['workerId'])))
        updateAMTHits.execute()

filesToApprove = [ANS_HITS_FILE, QUES_HITS_FILE]

for file in filesToApprove:
    if os.path.exists(file):
        #print file
        approveAllHits(file)

#db.close()
