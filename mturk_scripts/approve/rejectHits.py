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

    for index, row in uniqueApprove.iterrows():
        updateAMTHits = AMTHits.update(approve = 'approve')\
            .where((AMTHits.status == 'finished') & (AMTHits.approve == 'reviewReject') & (AMTHits.assignmentId == str(row['assignmentId'])) & (AMTHits.socketId == str(row['socketId'])) & (AMTHits.workerId == str(row['workerId'])))
        updateAMTHits.execute()


    reviewReject = hitsToApprove.loc[hitsToApprove['approve'] == 'reject']
    uniqueReviewReject = reviewReject.drop_duplicates(subset=['workerId', 'assignmentId', 'socketId'], keep = 'first')

    for index, row in uniqueReviewReject.iterrows():
        updateAMTHits = AMTHits.update(approve = 'reject')\
            .where((AMTHits.status == 'finished') & (AMTHits.approve == 'reviewReject') & (AMTHits.assignmentId == str(row['assignmentId'])) & (AMTHits.socketId == str(row['socketId'])) & (AMTHits.workerId == str(row['workerId'])))
        updateAMTHits.execute()

filesToApprove = [ANS_REJECTS_FILE, QUES_REJECTS_FILE]

for file in filesToApprove:
    if os.path.exists(file):
        #print file
        approveAllHits(file)

#db.close()
