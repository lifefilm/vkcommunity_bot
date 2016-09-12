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

from vkGroupApi import *
import config
from common import *

appName='strmama'

#######################################################

print 'Started...'+appName

# Словарь для команд

command = {
    'hi':{
        'txt':['привет','как дела', 'да', 'здравствуйте']
        ,'answer':'чем могу помочь?'
        ,'skip':True
    },
    'no':{
        'txt':['пока','нет','ничем','привет нет']
        ,'answer':'Пока, всего хорошего!'
        ,'skip':True
    },
    'thanks':{
        'txt':['спасибо','благодарю']
        ,'answer':'пожалуйста, Вам спасибо!'
        ,'sticker_id': '3'
        ,'skip':True
    },
    'bot':{
        'txt':['бот','ты бот','ты человек', 'ты кто']
        ,'answer':'я бот ;) strmama.ru'
        ,'skip':True
    },
    'help':{
        'txt':['help']
        ,'answer':''
    },
    'contacts':{
        'txt':['start','помощь','помогите', 'помогите мне','админ','контакты']
        ,'answer':
        '''
        Наш сайт: https://strmama.ru,
        Админ: https://vk.com/strmamy, @strmamy
        '''
    },
}

#список всех комананд, для помощи
ckeys = loadCommands (command)
command['help']['answer']='Чем помочь? Если нужны прямые контакты просто напишите боту "контакты"'


while True:

    lastMessages = messagesGet(200,appName)

    startWork(lastMessages, command, appName)

    time.sleep(1)
