# -*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup 
from telegram import KeyboardButton 
from telegram.ext import MessageHandler 
from telegram.ext import Filters 
from telegram.ext import RegexHandler 
import logging
import time
import threading
import re
import sys
import os
import collections
from telegram import constants
logging.basicConfig(format='%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO, filename=sys.argv[0] + '.log')
my_bot = Updater('<t o k e n>')


CMD = ['/start', 'Исх.код', 'Помощь', 'Do.Math']

def help_message(bot, update):
 result = ["Hey, %s!" % update.effective_user.first_name,
     "\rI can accept only these commands:"]
 for command in CMD:
  result.append(command)
 text = "\n\t".join(result)
 states[update.message.chat_id]['state'] = 1
 update.message.reply_text(text[0:constants.MAX_MESSAGE_LENGTH])

 
def source_message(bot, update):
 with open(sys.argv[0], 'r', encoding='utf-8') as fh:
  text = fh.read()
 text = re.sub(r"([t]oken) = .*", "'<t o k e n>')", text)
 text = re.sub(r"\s+[#].*", "", text)
 states[update.message.chat_id]['state'] = 1 
 i = 0
 while True:
  c = text[i:i+constants.MAX_MESSAGE_LENGTH]
  if not c:
   break
  update.message.reply_text(c)
  i += constants.MAX_MESSAGE_LENGTH
def foo():
 ops_ = {'state':1, 'op1':0, 'op2':0, 'opn':''}
 return ops_
states = collections.defaultdict(lambda: foo())
def reply_to_start_command(bot, update):
 first_name = update.effective_user.first_name
 last_name = update.effective_user.last_name
 reply_keyboard = [['Do.Math', 'Помощь', 'Исх.код']]
 text = "Привет, %s! \n Давай поиграем в математику" % first_name

 chat_id = update.message.chat_id
 states[chat_id]['state'] = 1
 
 update.message.reply_text(
  text, 
  reply_markup  = ReplyKeyboardMarkup(
   reply_keyboard,
   resize_keyboard = True,
   one_time_keyboard = True
  )
 )  
 

def do_math(bot, update, user_data):
  text = update.message.text
  chat_id = update.message.chat_id
  first_name = update.effective_user.first_name
  last_name = update.effective_user.last_name 
  logging.info("Пользователь {} {}, чат {}, ввел {}".format(first_name, last_name, chat_id, text))
  reply_keyboard = []
  ops = states[chat_id]
  
  if(ops['state'] == 1 or ops['state'] == 2):
   for i in range(0,10): 
    reply_keyboard.append(str(i))
   inv = 'Выберите %s операнд:' % ops['state']
   try:
    ops['op1'] = int(text)
   except:
    pass
   ops['state'] += 1

  elif (ops['state'] == 3):
   reply_keyboard = ['+','-','*','/','%']
   inv = 'Выберите операцию:'
   try:
    ops['op2'] = int(text)
   except:
    inv = 'Wrong input!'
    reply_keyboard = ['/start']
   ops['state'] += 1
   
  elif (ops['state'] == 4): 
   result = ''
   try:
    ops['opn'] = text
   except:
    inv = 'Wrong input!'
   
   try:
    query  = str(ops['op1']) + ops['opn'] + str(ops['op2'])
    result = eval(query)
    inv = 'Результат: %s = %s' % (query, result)
    reply_keyboard = ['/start']

   except:
    inv = 'Error on do math!'
    reply_keyboard = ['/start']
   ops['state'] = 1
   
  update.message.reply_text(
   inv, 
   reply_markup = ReplyKeyboardMarkup(
    [reply_keyboard],
    resize_keyboard = True,
    one_time_keyboard = True
   )
  )

def wrong_input(bot, update):
 text = update.message.text
 update.message.reply_text('Неверный ввод %s' % text)

 
my_bot.dispatcher.add_handler(
 CommandHandler("start",
  reply_to_start_command)
 )
 
my_bot.dispatcher.add_handler(
 RegexHandler(u'^(Исх.код)$', 
  source_message
 )
)

my_bot.dispatcher.add_handler(
 RegexHandler(u'^(Помощь)$', 
  help_message
 )
)

my_bot.dispatcher.add_handler(
 RegexHandler('^(Do\.Math)$', 
  do_math, 
  pass_user_data = True
 )
)

my_bot.dispatcher.add_handler(
 RegexHandler(
  '^([*+-/%0-9])$', 
  do_math,
  pass_user_data = True
 )
)

my_bot.dispatcher.add_handler(
 RegexHandler(
  '^(.*)$', 
  wrong_input
 )
)
my_bot.start_polling()