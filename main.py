import configparser
import pathlib
import telebot
from telebot import types
from client_api import *


from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

file_config = pathlib.Path('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DB', 'user')
password = config.get('DB', 'password')
bot_token = config.get('DB', 'bot_token')
base_url_soap = config.get('DB', 'base_url_soap')
base_url_rest = config.get('DB', 'base_url_rest')

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name} ({message.from_user.username})</b>'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('Товари')
    client = types.KeyboardButton('Кліенти')
    #website = types.KeyboardButton('Website')

    markup.add(item, client)
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.chat.type == 'private':

        if message.text == "Товари":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            by_code = types.KeyboardButton('За кодом')
            back = types.KeyboardButton('Назад')
            markup.add(by_code, back)
            bot.send_message(message.chat.id, 'Товари', reply_markup=markup)
        elif message.text == 'Кліенти':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            #by_phone = types.KeyboardButton('За номером телефона')
            #by_fio = types.KeyboardButton('ФИО')
            by_dc = types.KeyboardButton('За номером ДК')
            back = types.KeyboardButton('Назад')
            markup.add(by_dc, back)
            bot.send_message(message.chat.id, 'Кліенти', reply_markup=markup)
        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item = types.KeyboardButton('Товари')
            client = types.KeyboardButton('Кліенти')
            #website = types.KeyboardButton('Website')
            markup.add(item, client)
            bot.send_message(message.chat.id, "Назад", parse_mode='html', reply_markup=markup)
        elif message.text == "За кодом":
            item_no = bot.send_message(message.chat.id, 'Код товара:')
            bot.register_next_step_handler(item_no, find_by_item_no)
        elif message.text == "За номером ДК":
            dc_no = bot.send_message(message.chat.id, 'Номер дісконтної картки:')
            bot.register_next_step_handler(dc_no, find_by_dc_no)




if __name__ == '__main__':
    bot.polling(none_stop=True)
