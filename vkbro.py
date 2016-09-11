#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import json
import time
import random

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


vk_url="https://api.vkontakte.ru/method/"
vk_ver='5.53'
access_token='84bf24ce01548f2a85bcd4d2577d5b5cc6007b894b79d4f471f4f57346bd52aa08e0733ce81d69e2eafe2'
peer_id='-1747308378'


###################### ************************

def messagesGetDialogs():

    resp = requests.get(vk_url+'messages.getDialogs',
                    '&access_token={}&v={}'.format(access_token,vk_ver))

    result = resp.json()
    # print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))
    if 'response' in result:
        return result['response']['items']


def messagesGet(count=30):
    resp = requests.get(vk_url+'messages.get',
                    '&count={}&access_token={}&v={}'.format(count,access_token,vk_ver))

    result = resp.json()
    # print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))

    return result['response']['items']



def messagesGetHistory(user_id,start_message_id='',count=30):
    resp = requests.get(vk_url+'messages.getHistory',
                    '&user_id={}&start_message_id={}&peer_id={}&count={}&access_token={}&v={}'
                    .format(user_id, start_message_id, peer_id, count,access_token,vk_ver))

    result = resp.json()
    print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))

    return result['response']


def messagesSend(user_id,chat_id=1,message='',attachment='',stiker='20'):
    resp = requests.get(vk_url+'messages.send',
            '&user_id={}&peer_id={}&chat_id={}&message={}&attachment={}&access_token={}&v={}'
            .format(user_id,peer_id, chat_id,message,attachment,access_token,vk_ver))

    # result = resp.json()
    # print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))

    return resp

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

print 'Started...'


# Словарь для команд

command = {
    'bro':{
        'txt':['бро','bro', 'привет','как дела']
        ,'answer':'bro!'
        ,'image':'photo,photo-128566598_432688170'
    },
    'lesson':{
        'txt':['расписание','что сегодня', 'на неделю', 'lesson']
        ,'answer':'Расписание: - нет расписания'
    },
    'shutka':{
        'txt':['шутка','анекдот','цитата','ещё','еще']
        ,'answer':anekdot[int(round(random.random()*98))]
    },
    'help':{
        'txt':['помощь','help']
        ,'answer':'Команды: '
    },
}

#список всех комананд, для помощи
ckeysList=[]
for key,row in command.iteritems():
    ckeysList.append(row['txt'][0])

ckeys=', '.join(ckeysList)
command['help']['answer']='Команды: '+ckeys
print command['help']['answer']


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




    dial = messagesGet()

    for i in dial:

        status=0

        if int(i['read_state']) == 0:

            read = i['body'].encode('utf8')
            read = read.decode('utf8').lower()

            # перебераем в цикле наш словарь команд
            for cmd,otvet in command.iteritems():
                bro_image=''

                # если нашли совпадение команды
                if read in otvet['txt']:

                    if 'image' in otvet:
                        bro_image = otvet['image']

                    messagesSend(i['user_id'],i['id'],otvet['answer'],bro_image)

                    print '------------------------------'
                    print (str(i['user_id'])+': "'+read + '" --> ' + cmd)

                    status=1 # нашли команду и выходим
                    time.sleep(0.5)

                    break

            if status==0:
                    print read, ' - Не БРО'
                    messagesSend(i['user_id'],i['id'],'Прости, не понял тебя. (команды: помощь/шутка/расписание)')


    time.sleep(1)
