import socketio
from queue import Queue
from threading import Thread
import json


#import model, sample, encoder
sio = socketio.Client()

from ai import interact, train, utils


auth = {'username': 'bot@trevorbot.io', 'password': 'awesomesauce'}

if __name__ == "__main__":
    input_q = Queue()
    output_q = Queue()
    chatbot = Thread(target=interact.chatbot, args=(input_q, output_q,))
    chatbot.start()

    sio = socketio.Client()

    @sio.event
    def connect(): 
        print('Connected to sever')
        print(sio.sid)
        sio.emit('response_msg', {'type': 'connect', 'msg': 'User Connected', 'auth': auth})
    
    @sio.event
    def response_msg(message):
        print(message)
        name = message['user_name']
        message = message['message']
        if '@bot' not in message:
            print('[-] message not for bot' )
            return
        print("[-] Putting message into queue: ", message)
        input_q.put(message)
        reply = output_q.get()
        print("[-] Got reply: ", reply)
        if name != 'localbot':
            sio.emit('response_msg', {'user_name': 'localbot', 'type': 'msg',  'auth': auth, 'message': '<span class="badge badge-secondary">@{0}</span> {1}'.format(name, reply)})


    sio.connect('http://localhost:5000', namespaces=['/response_msg'])
    sio.wait()
