#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import json
import time
import random


vk_url="https://api.vkontakte.ru/method/"
access_token='84bf24ce01548f2a85bcd4d2577d5b5cc6007b894b79d4f471f4f57346bd52aa08e0733ce81d69e2eafe2'
peer_id='-1747308378'

###################### ************************

def messagesGetDialogs():

    resp = requests.get(vk_url+'messages.getDialogs',
                    '&access_token={}&v=5.53'.format(access_token))

    result = resp.json()
    # print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))
    if 'response' in result:
        return result['response']['items']


def messagesGet(count=30):
    resp = requests.get(vk_url+'messages.get',
                    '&count={}&access_token={}&v=5.53'.format(count,access_token))

    result = resp.json()
    print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))

    return result['response']['items']



def messagesGetHistory(user_id,start_message_id='',count=30):
    resp = requests.get(vk_url+'messages.getHistory',
                    '&user_id={}&start_message_id={}&peer_id={}&count={}&access_token={}&v=5.53'
                    .format(user_id, start_message_id, peer_id, count,access_token))

    result = resp.json()
    print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))

    return result['response']


def messagesSend(user_id,chat_id=1,message='',attachment='',stiker='20'):
    resp = requests.get(vk_url+'messages.send',
            '&user_id={}&peer_id={}&chat_id={}&message={}&attachment={}&access_token={}&v=5.53'
            .format(user_id,peer_id, chat_id,message,attachment,access_token))

    result = resp.json()
    print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))

    return result

def loadAnekdot(count=100):

    import html2text

    resp = requests.get('http://www.umori.li/api/get?site=bash.im&name=bash&num={}'.format(count))

    result = resp.json()

    anekdot=[]

    for row in result:
        html=row['elementPureHtml']
        txt= html2text.html2text(html).strip().encode('utf-8')
        anekdot.append(txt)
    # print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))
    return anekdot

###################### ************************

anekdot=loadAnekdot()

while True:

    dialogs=messagesGetDialogs()
    # mg=messagesGet()

    userList={}
    user={}

    for items in dialogs:
        user_id = items['message']['user_id']
        user['msg_id'] = items['message']['user_id']
        user['status'] = 0

        userList[user_id]=user

    # for user_id,j in userList.iteritems():
    #     # Первое сообщение
    #
    #     ustxtany = ['']
    #     textw1 = 'Добро пожаловать, мы скинем вам рассписание скажите свою группу'
    #
    #     if j['status'] == 0:
    #         messagesSend(user_id,j['msg_id'],textw1,'photo,photo-128566598_432688189')
    #         j['status'] = 0


    # Словарь для команд
    txt={}
    txt['bro'] = ['бро','bro','Бро','Bro','BRO', 'БРО']
    txt['lesson'] = ['lesson','расписание','что сегодня', 'на неделю']
    txt['shutka'] = ['шутка','анекдот','цитата','ещё','еще']


    dial = messagesGet()

    for i in dial:

        print '------------------ user_id:', i['user_id']

        if int(i['read_state']) == 0:

            read = i['body'].encode('utf8')
            if read in txt['bro']:
                textbro = 'bro!'
                messagesSend(i['user_id'],i['id'],textbro,'photo,photo-128566598_432688170')
                time.sleep(1)
                print read, ' - Шлем бро!'

            elif read in txt['lesson']:
                textbro = 'Расписание: - нет расписания'
                messagesSend(i['user_id'],i['id'],textbro)
                time.sleep(1)
                print read, ' - Шлем расписание!'

            elif read in txt['shutka']:
                rnd= int(round(random.random()*100))
                textbro = anekdot[rnd]
                print textbro
                messagesSend(i['user_id'],i['id'],textbro)
                time.sleep(1)
                print read, ' - Шлем shutka!'

            else:
                print read, ' - Не БРО'
                messagesSend(i['user_id'],i['id'],'Прости не понял тебя')



    # for user_id,j in userList.iteritems():
    #
    #     print '------------------ user_id:', user_id
    #     msg=messagesGetHistory(user_id, j['msg_id'])
    #
    #     if msg['count']>0:
    #
    #         read = msg['items']['body'].encode('utf8')
    #         if read == 'бро':
    #             messagesSend(msg['user_id'],chat_id['id'],textbro)
    #             print read, ' - Шлем бро!'
    #         else:
    #             print read, ' - Не БРО'
    #     else:
    #         print 'No count'


    time.sleep(1)
