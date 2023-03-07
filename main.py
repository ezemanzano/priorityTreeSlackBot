import slack
from flask import Flask, Response
from flask import request
from slackeventsapi import SlackEventAdapter

import os

from database import list_items,last_order,last_id,add_item,delete_item,orderPriorityTree,checkIfAllExist,getAmount,editOrderPriorityTree

SLACK_TOKEN=str(os.getenv("SLACK_TOKEN"))
app = Flask(__name__)

client = slack.WebClient(token=SLACK_TOKEN)



@app.route('/list', methods=['GET','POST'])
def list():
    list = list_items()
    stringResponse = 'Priority tree :christmas_tree:  \n'
    stack = ""
    for x in list:
        stack =  stack + x['order'] + '. *' + x['name'].upper() +"* (id: "+x['id']+")" + ' \n'
    client.chat_postMessage(channel='prioritytreebot',text=stringResponse + stack)
    return Response(),200

@app.route('/add', methods=['GET','POST'])
def add():
    if(len(request.form['text']) > 0):
        last = last_order()
        lastId = last_id()        
        if (add_item({'name': request.form['text'], 'order' : last+1, 'id' : lastId+1}) != None):
            client.chat_postMessage(channel='prioritytreebot',text=" Se agregó " + request.form['text'] + " correctamente :ok_hand::skin-tone-2: ")
    else:
        client.chat_postMessage(channel='prioritytreebot',text='Necesito un nombre :sob: ')
    return Response(),200


@app.route('/delete', methods=['GET','POST', 'DELETE'])
def delete():
    if(len(request.form['text']) > 0):
        if (delete_item(request.form['text']) != None):
            orderPriorityTree()
            client.chat_postMessage(channel='prioritytreebot',text=" Se eliminó correctamente :ok_hand::skin-tone-2: ")
    else:
        client.chat_postMessage(channel='prioritytreebot',text='Necesito un nombre :sob: ')
    return Response(),200


@app.route('/modify', methods=['GET','POST'])
def modify():
    if(len(request.form['text']) > 0):
        params = request.form['text'].split(',')
        amount = getAmount()
        if(len(params) == amount):     
            if checkIfAllExist(params):       
                editOrderPriorityTree(params)
                client.chat_postMessage(channel='prioritytreebot',text=" Se modifico correctamente :ok_hand::skin-tone-2: ")
            else:
                client.chat_postMessage(channel='prioritytreebot',text=" Id inexistente")
        else:
            client.chat_postMessage(channel='prioritytreebot',text='La cantidad de ids ingresados no coincide con los items registrados ')
    else:
        client.chat_postMessage(channel='prioritytreebot',text='Faltan parametros ')
    return Response(),200


@app.route('/publish', methods=['GET','POST'])
def publish():
    list = list_items()
    stringResponse = 'Priority tree :christmas_tree:  \n'
    stack = ""
    for x in list:
        stack =  stack + x['order'] + '. *' + x['name'].upper() + '* \n'
    client.chat_postMessage(channel='sistemas',text=stringResponse + stack)
    return Response(),200

if __name__ == "__main__":
    app.run(debug=True)