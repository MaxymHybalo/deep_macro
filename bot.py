import telebot
from telebot import types
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.INFO) # Outputs debug messages to console.

bot = None
chat_id = 277698748
token = '1940828974:AAGJT4OGhSe3L91elGKEdfzBd-ymbOcWmcg'
bot = telebot.TeleBot(token)

def setup():
	pass
	# bot = telebot.TeleBot(token)

	# print('inited')

	# @bot.message_handler(commands=['start', 'help'])
	# def init(message):
	# 	print(message)
	# 	bot.reply_to(message, "Howdy, how are you doing?")
	# 	chat_id = message.chat.id

	# bot.polling()

def notify(bot=bot, chat_id=chat_id, **params):
	print('Try send meesage', bot, params, chat_id)
	if bot is None:
		return
	bot.send_message(chat_id, 'Some action in window: {} ({})'.format(params['hwnd'], params['data']))
