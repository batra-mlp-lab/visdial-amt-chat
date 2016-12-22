var config = require('./config')
var express = require('express');
var app = express();
var mysql     =    require('mysql');
var moment = require('moment');
var async = require('async');
var us = require('underscore');
var knex = require('knex')({
    client: 'mysql',
    connection: {
        host     : '127.0.0.1',
        user     : config.db.user,
        password : config.db.pass,
        database : config.db.name,
        charset  : 'utf8'
    }
});

var redis = require("redis");
var client = redis.createClient(config.redis.port);
client.auth(config.redis.pass, function(){});
var REDIS_LIST = config.redis.list;

knex.schema.hasTable('amthits').then(function(exists) {
    console.log('AMTHits Table Exists: '+ exists);
    knex.select().table('amthits').then(function(result){});
    myDate =  moment(new Date()).format("YYYY-MM-DD HH:mm:ss");
    console.log(myDate);
});


var http = require('http').Server(app);
var io = require('socket.io')(http);

var activeUsers = {};
var numUsers = 0;

var userQueue = [];
app.use(express.static('semanticui'));
app.use(express.static('css'));

var path = config.root;
app.use(express.static(path));
app.use(express.static('js'));
app.use(express.static('static'));
app.use(express.static(path + 'static/dataset/')); // TODO

app.get('/', function(req, res){
  res.sendfile('index.html');
});

function getUid(){
    return Math.random().toString(36);
}

io.on('connection', function(socket){

    console.log('a user connected');

    socket.partnerId = '';
    socket.noOfMsg1st = 0;
    socket.noOfMsg2nd = 0;

    // when the client emits 'add user', this listens and executes
    socket.on('add user', function (msg) {

        // we store the username in the socket session for this client
        // socket.username = msg['personName'];
        socket.workerId = msg['workerId'];
        socket.partnerId = '';
        socket.role = '';
        socket.assignmentId = msg['assignmentId'];
        socket.hitId = msg['hitId'];

        console.log('WorkerId: ' + socket.workerId);
        console.log('AssignmentId: ' +  socket.assignmentId);
        // add the client's username to the global list
        activeUsers[socket.id] = socket;
        ++numUsers;

        var isPaired = false;

        if (userQueue.length == 0) {
            socket.role = 'question';
            userQueue.push(socket.id);
            console.log('First User in the queue: '+ socket.workerId);
        }
        else
        {
            var flag = 0;
            var i = 0;
            async.series([
                function(callback){
                    while(i < userQueue.length)
                    {
                        var userPairId = '';
                        userPairId = userQueue.shift();
                        if(activeUsers[userPairId]==undefined) { // If there is only one user in the queue.
                            continue;
                        }
                        if(activeUsers[userPairId].workerId == socket.workerId)
                        {
                            // Checking if the same user is try to connect to itself. In which case don't connect and add him back to the queue.
                            console.log('Worker 1: ' + socket.workerId);
                            console.log('Worker 2: ' + activeUsers[userPairId].workerId);
                            i= i+1;
                            userQueue.push(userPairId);
                        }
                        else
                        {
                            /*knex.select().table('amthits').where(function() {
                                                this.where({'workerId':socket.workerId})
                                                .andWhere({'assignmentId': socket.assignmentId})
                            })
                            .then(function (resp) {
                                if(resp.length!=0){
                                    socket.emit('error', {errorMsg: "You already have attempted a chat with this assignment. Please choose another."});
                                }
                            });*/


                            console.log('Separate Worker 1: ' + socket.workerId);
                            console.log('Separate Worker 2: ' + activeUsers[userPairId].workerId);

                            if(userPairId in activeUsers)
                            {
                                activeUsers[userPairId].partnerId = socket.id;
                                activeUsers[userPairId].key = socket.id + userPairId;
                                activeUsers[userPairId].image_name = 'sample';
                                activeUsers[userPairId].role  = 'answer';

                                socket.partnerId = userPairId;

                                activeUsers[socket.id].partnerId = userPairId;
                                activeUsers[socket.id].key = socket.id + userPairId;
                                activeUsers[socket.id].image_name = 'sample';
                                activeUsers[socket.id].role  = 'question';

                                isPaired = true;
                                var image_url="";
                                var found_image = false;
                                numList = us.range(60); // Will change according to the number of images you launch.
                                var foundFlag  = false;
                                async.eachSeries(numList,
                                function(item, callback) {
                                    if(foundFlag == false) {    // Pop from the queue and check if either user has done that image before.
                                        client.rpop(REDIS_LIST, function(err, res) {
                                            knex.select().table('amthits').where(function() {
                                                this.where({'workerId':activeUsers[userPairId].workerId})
                                                .orWhere({'workerId': socket.workerId})
                                            })
                                            .innerJoin('image', 'amthits.image_id', '=', 'image.imageId')
                                            .andWhere('image.imageName', res)
                                            .then(function(resp){
                                                //console.log(resp)
                                                //console.log('Image Name: ' + res);
                                                console.log('SQL Check: ' + resp.length);
                                                if(resp.length!=0){
                                                    client.lpush(REDIS_LIST, res);
                                                }
                                                else {
                                                    foundFlag = true;
                                                    image_url = res;
                                                    console.log('Before caption')
                                                    console.log('Image: ' + res);

                                                    //knex.select('image.imageId').from('image').where('image.imageName', '=', res)
                                                    knex.select('caption.caption', 'image.imageId')
                                                    .table('caption').innerJoin('image', 'caption.image_id', '=', 'image.imageId')
                                                    .where('image.imageName', '=', res)
                                                    .then(function(cap){
                                                        console.log(cap);
                                                        // add the first person's HIT details
                                                        knex('amthits')
                                                            .insert({
                                                            id: getUid(),
                                                            socketId: socket.key,
                                                            image_id: cap[0]['imageId'],
                                                            workerId: socket.workerId,
                                                            assignmentId:  socket.assignmentId,
                                                            hitId: socket.hitId,
                                                            approve: 'notApprove',
                                                            status: 'started',
                                                            created_at: moment().unix()
                                                            }).then(function(result){
                                                                knex('amthits')
                                                                .insert({   // add the second person's HIT details
                                                                        id: getUid(),
                                                                        socketId: activeUsers[userPairId].key,
                                                                        image_id: cap[0]['imageId'],
                                                                        workerId: activeUsers[userPairId].workerId,
                                                                        assignmentId:  activeUsers[userPairId].assignmentId,
                                                                        hitId: activeUsers[userPairId].hitId,
                                                                        approve: 'notApprove',
                                                                        status: 'started',
                                                                        created_at: moment().unix()
                                                                    })
                                                                .then(function(result){
                                                                    // finally, emit the messages.
                                                                    activeUsers[userPairId].image_name = image_url;
                                                                    activeUsers[socket.id].image_name = image_url;
                                                                    activeUsers[socket.id].push = true;
                                                                    socket.emit('paired', {
                                                                        'partnerId' : userPairId,
                                                                        'key' : socket.id + userPairId,
                                                                        'image_url': 'train2014/' + image_url,
                                                                        'role': 'question',
                                                                        'caption': cap[0]['caption']
                                                                    });

                                                                    activeUsers[userPairId].emit('paired', {
                                                                        'partnerId' :socket.id,
                                                                        'key' : socket.id + userPairId,
                                                                        'role': 'answer',
                                                                        'caption': cap[0]['caption']
                                                                    });
                                                                    console.log('assignmentId:' + socket.assignmentId);


                                                                });
                                                        });

                                                    });
                                                }
                                                callback();
                                            });

                                        });
                                    }
                                    else{
                                        callback();
                                    }
                                },
                                function(err){});
                                flag = 1;
                                break;
                                if( flagfound==false) {
                                    console.log('All images tried by this user: ' + socket.workerId);
                                    socket.emit('error', {errorMsg: "You completed tasks for all the images in the database. Thank you for all your work. Please try again later."});
                                }
                            }
                        }
                    }

                    callback(null,null);
                },
                function(callback){
                    if (flag==0)
                    {
                        userQueue.push(socket.id);
                    }
                    callback(null,null);
                }
            ],
            function(err,results) {
                console.log('Error') // This is not really an error.
                //console.log('UserQueue: '+ userQueue);
            });
        }
    });

    // when a chat message is sent. This is emmitted by $(send) in index.html
    socket.on('chat message', function(msg){
        var f = 'chatmsg : ';
        socket.noOfMsg1st = socket.noOfMsg1st + 1;
        console.log(JSON.stringify(msg));
        var ig = socket.image_name;
        console.log(ig);
        if (socket.partnerId in activeUsers) {
            activeUsers[socket.partnerId].noOfMsg2nd = activeUsers[socket.partnerId].noOfMsg2nd + 1;
            activeUsers[socket.partnerId].emit('receive message', {'message' : msg['msg'], 'noOfMsg': socket.noOfMsg1st});
            console.log(f + 'message count: ' + socket.noOfMsg2nd + socket.noOfMsg1st);
            var ig = activeUsers[socket.partnerId].image_name;
        }

        knex.select('id').from('amthits')
        .where('hitId', '=', msg['hitId'])
        .andWhere('assignmentId','=', msg['assignmentId'])
        .andWhere('workerId', '=', msg['workerId'])
        .andWhere('socketId', '=', socket.key)
        .then(function(hitResult){
            knex.select('imageId','numHitsFinished').from('image').where('image.imageName', '=', ig)
            .then(function(img){
                console.log(JSON.stringify(img));

                if(msg['role'] == 'question'){
                    console.log(f + 'in question');
                    knex('question').insert({
                        id: getUid(),
                        question: msg['msg'],
                        image_id: img[0]['imageId'],
                        annotationId_id: hitResult[0]['id'],
                        sequenceId: msg['seqId'],
                        socketId: socket.key,
                        sourceId: socket.id,
                        destId: socket.partnerId,
                        // timestamp: moment(new Date()).format("YYYY-MM-DD HH:mm:ss")
                        created_at: moment().unix()
                    })
                    .then(function(result){});

                }
                else{
                    console.log(f + 'in answer');
                    knex('question')
                    .where('question.socketId', '=', socket.key)
                    .andWhere('question.sequenceId', '=', msg['seqId'])
                    .select('question.id', 'question.image_id')
                    .then(function(quesResult){
                        if(quesResult.length == 0){ //questioner disconnected, so you won't have any question for this answ
                            knex('answer').insert({
                                id: getUid(),
                                answer: msg['msg'],
                                question_id: '',
                                image_id: img[0]['imageId'],
                                annotationId_id: hitResult[0]['id'],
                                sequenceId: msg['seqId'],
                                socketId: socket.key,
                                sourceId: socket.id,
                                destId: socket.partnerId,
                                created_at: moment().unix()
                            })
                            .then(function(result){});
                        }
                        else{   //question exists
                            // console.log(quesResult[0]);
                            knex('answer').insert({
                                id: getUid(),
                                answer: msg['msg'],
                                question_id: quesResult[0]['id'], //select the question id of the last question asked.
                                image_id: img[0]['imageId'],
                                annotationId_id: hitResult[0]['id'],
                                sequenceId: msg['seqId'],
                                socketId: socket.key,
                                sourceId: socket.id,
                                destId: socket.partnerId,
                                created_at: moment().unix()
                            })
                            .then(function(result){});
                        }
                    });
                }
            });

        });

    });

    socket.on('finish hit', function(msg) {

        console.log('HIT submitted');
        if('push' in socket) {
            if(socket['push']==true) {
                socket['push'] = false;
            }
        }
        knex.select('image.ImageId').from('image').where('image.imageName', '=', socket.image_name)
        .then(function(img){
            // console.log(JSON.stringify(img));
            knex('amthits').where('image_id', '=', img[0]['ImageId'])
             .andWhere('assignmentId', '=', socket.assignmentId)
             .andWhere('hitId','=', socket.hitId)
             .andWhere('workerId','=', socket.workerId)
             .andWhere('socketId','=', socket.key)
             .update({
                status: 'finished',
                completed_at: moment().unix()
            }).then(function(result){   // Increment the number of hits finished.
                console.log('Status: Finished')

                knex('amthits').count('id').where('image_id', '=', img[0]['ImageId'])
                .andWhere('status', '=', 'finished')
                .then(function(cntResult){
                     cnt = parseInt(cntResult[0]['count(`id`)']);
                     cnt = (cnt + 1)/2;
                     cnt = parseInt(cnt);
                     knex('image').where('imageId', '=', img[0]['ImageId'])
                     .update({
                        numHitsFinished: cnt.toString()
                    }).then(function(result){
                        knex('feedback').insert({
                            workerId: msg['workerId'],
                            hitId: msg['hitId'],
                            assignmentId: msg['assignmentId'],
                            sequenceId: socket.key,
                            feedback: msg['feedback']
                        })
                        .then({})

                    });  // Increment the number of hits finished.
                });
            });
        });

    });

    socket.on('disconnect', function() {
        console.log('Got disconnected!');
        console.log(socket.partnerId);
        if('push' in socket) {
            if(socket['push'] == true) {
                 client.lpush(REDIS_LIST, socket['image_name']);
            }
        }
        // ToDo: Finish HIT here!
        if(socket.partnerId !='' || socket.partnerId==undefined) {
            if(socket.partnerId in activeUsers) {
                activeUsers[socket.partnerId].partnerId = '';
                activeUsers[socket.partnerId].emit('disconnected partner', {'disable':'true'});
            }
        }
        delete activeUsers[socket.id];
    });

    socket.on("typing", function(message) {
        if (socket.partnerId in activeUsers) {
            if(message){
                activeUsers[socket.partnerId].emit('is typing', {isTyping: 'yes'});
            }
            else{
                 activeUsers[socket.partnerId].emit('is typing', {isTyping: 'no'});
            }
        }
    });

});

http.listen(5000, function(){
  console.log('listening on *:5000');
});
