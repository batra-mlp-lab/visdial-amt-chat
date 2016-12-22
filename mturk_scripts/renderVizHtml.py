###
# A somewhat ugly script to visualize the latest collected data
###

import os
import sys
import json
import datetime
import MySQLdb as mdb

NUM_HITS_VIZ = 100

config = json.load(open('/path/to/visdial-amt-chat/mturk_scripts/config.json', 'r')) # TODO

FROM_TIMESTAMP = config['from_timestamp']

con = mdb.connect(host="localhost", user=config['db_user'], db=config['db_name'], passwd=config['db_pass'])
cur = con.cursor()

query = "SELECT amthits.* FROM amthits INNER JOIN (SELECT image_id, count(image_id) AS cnt FROM amthits WHERE status = 'finished' GROUP BY image_id) C ON amthits.image_id = C.image_id WHERE amthits.status = 'finished' AND C.cnt = 2 AND amthits.created_at >= %d;" % FROM_TIMESTAMP
cur.execute(query)

hits = {}
for i in range(cur.rowcount):
    row = cur.fetchone()
    hits[row[1]] = {'image_id': row[11], 'caption': '', 'questions': [], 'answers': []}

for i in hits:
    query = "SELECT * FROM question WHERE socketId = '%s' AND sourceId != '' and destId != '' ORDER BY CAST(sequenceId AS UNSIGNED) ASC;" % i
    cur.execute(query)
    for j in range(min(10, cur.rowcount)):
        row = cur.fetchone()
        hits[i]['questions'].append(row[1])
    query = "SELECT * FROM answer WHERE socketId = '%s' AND (destId != '' OR (destId = '' AND sequenceId = '10')) ORDER BY CAST(sequenceId AS UNSIGNED) ASC;" % i
    cur.execute(query)
    for j in range(min(10, cur.rowcount)):
        row = cur.fetchone()
        hits[i]['answers'].append(row[1])
    query = "SELECT caption FROM caption WHERE image_id = '%s';" % hits[i]['image_id']
    cur.execute(query)
    row = cur.fetchone()
    hits[i]['caption'] = row[0]

html = '<!DOCTYPE html><html><head><title>VisDial data</title><link rel="stylesheet" type="text/css" href="//computing.ece.vt.edu/~abhshkdz/static/css/bootstrap.min.css"></head><body><div class="container-fluid">'
html += '<div class="row"><div class="col-lg-12"><h1 style="font-size:2.5em;">VisDial data</h1></div></div>'
html += '<div class="row"><div class="col-lg-12">%d images. After %s.</div></div>' % (len(hits.keys()), datetime.datetime.fromtimestamp(FROM_TIMESTAMP).strftime('%Y-%m-%d %H:%M:%S'))
html += '<hr>'
html += '<div class="row"><div class="col-lg-12"><table class="table table-striped">'
html += '<thead><tr><th>Image</th><th>Caption</th><th>Questions</th><th>Answers</th></tr></thead>'
html += '<tbody>'
for i in hits:
    html += "<tr>"
    html += "<td><img class='img-responsive' src='https://vision.ece.vt.edu/mscoco/images/train2014/COCO_train2014_%012d.jpg'>%s</td>" % (int(hits[i]['image_id']), i)
    html += "<td>%s</td>" % hits[i]['caption']
    html += "<td><ol>"
    for j in range(min(10, len(hits[i]['questions']))):
        html += "<li>%s</li>" % hits[i]['questions'][j]
    html += "</td></ol>"
    html += "<td><ol>"
    for j in range(min(10, len(hits[i]['answers']))):
        html += "<li>%s</li>" % hits[i]['answers'][j]
    html += "</td></ol>"
    html += "</tr>"

html += "</tbody></table></div></div></div></body></html>"

with open('/path/to/visdial-amt-chat/mturk_scripts/viz/hits_%d.html' % FROM_TIMESTAMP, 'w') as tf: # TODO, also create `viz` folder
    tf.write(html)
