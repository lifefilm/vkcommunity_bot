#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import requests
import json
import time
import random

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#######################################################

import config

access_token = config.life_token
peer_id = config.life_peer_id

vk_url="https://api.vkontakte.ru/method/"
vk_ver='5.53'

#######################################################

def messagesGetDialogs(access_token=access_token):

    resp = requests.get(vk_url+'messages.getDialogs',
                    '&access_token={}&v={}'.format(access_token,vk_ver))

    result = resp.json()
    # print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))
    if 'response' in result:
        return result['response']['items']


def messagesGet(count=30,access_token=access_token):
    resp = requests.get(vk_url+'messages.get',
                    '&count={}&access_token={}&v={}'.format(count,access_token,vk_ver))

    result = resp.json()
    # print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))

    return result['response']['items']



def messagesGetHistory(user_id,start_message_id='',count=30,access_token=access_token):
    resp = requests.get(vk_url+'messages.getHistory',
                    '&user_id={}&start_message_id={}&peer_id={}&count={}&access_token={}&v={}'
                    .format(user_id, start_message_id, peer_id, count,access_token,vk_ver))

    result = resp.json()
    print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))

    return result['response']


def messagesSend(user_id,chat_id=1,message='',attachment='',stiker='20',access_token=access_token):
    resp = requests.get(vk_url+'messages.send',
            '&user_id={}&peer_id={}&chat_id={}&message={}&attachment={}&access_token={}&v={}'
            .format(user_id,peer_id, chat_id,message,attachment,access_token,vk_ver))

    # result = resp.json()
    # print (json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False))

    return resp
