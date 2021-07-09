#!/usr/bin/env python
# encoding: utf-8
"""
@version: v1.0
@author: W_H_J
@license: Apache Licence
@contact: 415900617@qq.com
@software: PyCharm
@file: flaskIOTest.py
@time: 2019/2/20 12:04
@describe: flask-socketio 服务端
"""
import sys
import os
import sqllocal
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO()
socketio.init_app(app)
con = sqlite3.connect(r"E:/sqlite3/test.db")
cur = con.cursor()
name_space = '/test'
ins = r"insert into version (S,R,C,old,new,murder) values ({0},{1},{2},'{3}','{4}','{5}')"
upd = r'update version set new = "{0}" where S = {1} and R = {2} and C = {3};'

@app.route('/')
def get_abc():
    """加载接收消息页面"""
    return render_template('index.html')


@app.route('/push')
def push_once():
    """广播消息
    发送消息：http://127.0.0.1:5000/push?msg=a
    """
    event_name = 'message'
    data = request.args.get("msg")
    broadcasted_data = {'data': data}
    print("publish msg==>", broadcasted_data)
    socketio.emit(event_name, broadcasted_data, broadcast=True, namespace=name_space)
    socketio.emit('abcde', broadcasted_data, broadcast=True, namespace=name_space)
    return 'send msg successful!'


@socketio.on('updater', namespace=name_space)
def test_message(message):
    print('updater message', message)
    data = eval((message['data']))
    r = data["row"]
    c = data["column"]
    old = data["oldValue"]
    new = data["newValue"]
    if sqllocal.select(0,r,c) == None:
        print('insert:\n')
        if new != sqllocal.select(0,r,c):
            query = ins.format(0,r,c,old,new,'admin')
            cur.execute(query)
            con.commit()
            socketio.emit('update', message['data'], namespace=name_space)
    else:
        print('update!\n')
        query = upd.format(new, 0, r, c)
        cur.execute(query)
        con.commit()
        socketio.emit('update', message['data'], namespace=name_space)

@socketio.on('update', namespace=name_space)
def test_message(message):
    print('update message', message)


@socketio.on('connect', namespace=name_space)
def connected_msg():
    """客户端连接"""
    print('client connected!', request.sid)
    data = sqllocal.init()
    for i in data:
        form = '"row":{0}, "column":{1}, "oldValue":"{2}", "newValue":"{3}", "isRefresh":"{4}"'
        dat = '{'+form.format(i[1],i[2],i[3],i[4],'true') + '}'
        # print('asd:', dat)
        socketio.emit('update', dat, namespace=name_space)


@socketio.on('disconnect', namespace=name_space)
def disconnect_msg():
    """客户端离开"""
    print('client disconnected!')


if __name__ == '__main__':
    print("conent http://172.22.116.27:5000")
    socketio.run(app, host='172.22.116.27', port=5000)
    cur.close()