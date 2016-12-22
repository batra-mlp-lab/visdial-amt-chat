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

def addrow(df, row):
    return df.append(pd.DataFrame(row), ignore_index=True)

def getAllAnsHits():
    print 'In getAllAnsHits'
    allHits = AMTHits.select(AMTHits, Answer)\
             .join(Answer)\
             .where((AMTHits.status == 'finished') & (AMTHits.approve == 'reviewReject'))
    listOfColumns = [
        'id',
        'workerId',
        'hitId',
        'assignmentId',
        'socketId',
        'question',
        'answer',
        'approve',
        'answer.image_id',
        'answer.sequenceId',
        'answer.socketId',
        'answer.sourceId',
        'answer.created_at',
    ]

    aHits = pd.DataFrame()

    for hit in allHits:

        try:
            ques = Question.select(Question, Answer)\
                .join(Answer)\
                .where((Answer.socketId == hit.answer.socketId) & (Answer.socketId == Question.socketId) & (Question.sequenceId == hit.answer.sequenceId))
            q = ques[0].question
        except:
            q = ''

        row = [
        hit.id,
        hit.workerId,
        hit.hitId,
        hit.assignmentId,
        hit.socketId,
        q,
        hit.answer.answer,
        hit.approve,
        hit.answer.image.imageId,
        hit.answer.sequenceId,
        hit.answer.socketId,
        hit.answer.sourceId,
        hit.answer.created_at
        ]

        aHits = aHits.append(row)

    num_rows = (aHits.shape[0]/13)
    ans = pd.DataFrame(aHits.values.reshape(num_rows,13))
    ans.columns = listOfColumns
    ans.to_csv(ANS_REJECTS_FILE)

    print ANS_REJECTS_FILE + ' created.'

def getAllQuesHits():
    print 'In getAllQuesHits'
    allHits = AMTHits.select(AMTHits, Question)\
             .join(Question)\
             .where((AMTHits.status == 'finished') & (AMTHits.approve == 'reviewReject'))
    listOfColumns = [
        'id',
        'workerId',
        'hitId',
        'assignmentId',
        'socketId',
        'question',
        'approve',
        'question.image_id',
        'question.sequenceId',
        'question.socketId',
        'question.sourceId',
        'question.created_at',
    ]

    aHits = pd.DataFrame()

    for hit in allHits:

        row = [
        hit.id,
        hit.workerId,
        hit.hitId,
        hit.assignmentId,
        hit.socketId,
        hit.question.question,
        hit.approve,
        hit.question.image.imageId,
        hit.question.sequenceId,
        hit.question.socketId,
        hit.question.sourceId,
        hit.question.created_at
        ]

        aHits = aHits.append(row)

    num_rows = (aHits.shape[0]/12)
    ans = pd.DataFrame(aHits.values.reshape(num_rows,12))
    ans.columns = listOfColumns
    ans.to_csv(QUES_REJECTS_FILE)

    print QUES_REJECTS_FILE + ' created.'

getAllAnsHits()
getAllQuesHits()

