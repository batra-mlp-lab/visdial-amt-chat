import MySQLdb as mdb
import json
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
             .where((AMTHits.status == 'finished') & (AMTHits.approve == 'notApprove'))\
             .order_by(AMTHits.socketId, Answer.sequenceId.asc())
             # .where(AMTHits.status == 'started' and AMTHits.approve == 'approve')

    print('Finish Answers')
    print 'No. of A Hits: ', len(allHits)
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
    count = 0
    for hit in allHits:
        # if(hit.status == 'started'):
        try:
            ques = Question.select(Question, Answer)\
                .join(Answer)\
                .where((Answer.socketId == hit.answer.socketId) and (Answer.socketId == Question.socketId) and (Answer.image == hit.answer.image))

            rowQues = ''
            for q in ques:
                if q.sequenceId == hit.answer.sequenceId:
                    rowQues = q.question
                    #print 'Question : ' + rowQues
                    #print 'Answer : ' + hit.answer.answer
                    break
                rowQues = ''
        except:
            rowQues = ''

        row = [
        hit.id,
        hit.workerId,
        hit.hitId,
        hit.assignmentId,
        hit.socketId,
        rowQues,
        hit.answer.answer,
        hit.approve,
        hit.answer.image.imageId,
        hit.answer.sequenceId,
        hit.answer.socketId,
        hit.answer.sourceId,
        hit.answer.created_at
        ]

        aHits = aHits.append(row)
        count += 1
        if(count%100 == 0):
            print count

    num_rows = (aHits.shape[0]/13)
    ans = pd.DataFrame(aHits.values.reshape(num_rows,13))
    ans.columns = listOfColumns
    ans.to_csv(ANS_HITS_FILE, encoding='utf-8')

    print ANS_HITS_FILE + ' created.'

def getAllQuesHits():
    print 'In getAllQuesHits'
    allHits = AMTHits.select(AMTHits, Question)\
             .join(Question)\
             .where((AMTHits.status == 'finished') & (AMTHits.approve == 'notApprove'))\
             .order_by(AMTHits.socketId, Question.sequenceId.asc())
             # .where(AMTHits.approve == 'approve')

    print('Finish Questions')
    print 'No. of Q Hits: ', len(allHits)
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
    count = 0
    for hit in allHits:
        # if(hit.status == 'started'):
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
        count += 1
        if(count%100 == 0):
            print count

    num_rows = (aHits.shape[0]/12)
    ans = pd.DataFrame(aHits.values.reshape(num_rows,12))
    ans.columns = listOfColumns
    ans.to_csv(QUES_HITS_FILE, encoding='utf-8')

    print QUES_HITS_FILE + ' created.'

getAllQuesHits()
getAllAnsHits()
