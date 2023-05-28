import requests
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from main import username, password, base_url_soap, base_url_rest, bot, types


def find_by_item_no(message):
    session = Session()
    session.verify = False
    session.auth = HTTPBasicAuth(username, password)
    transport = Transport(session=session)
    client = Client(base_url_soap + '_Items?wsdl', transport=transport)
    # print(client.wsdl.dump())
    item = client.service.Get_Item('IMP', message.text, '')

    if item == 'No items':
        bot.send_message(message.chat.id, f'На жаль за кодом: {message.text} - товару не знайшли', parse_mode='html')
        return

    tree = ET.fromstring(item)

    item_txt = 'Найменування: ' + '<b>' + tree.find('НаименованиеПолное').text + '</b>\n' + \
               'Артикул: ' + '<b>' + tree.find('Артикул').text + '</b>\n' + \
               'Країна: ' + '<b>' + tree.find('Страна').text + '</b>\n' + \
               'Виробник: ' + '<b>' + tree.find('Производитель').text + '</b>\n' + \
               'Ціна РРЦ: ' + '<b>' + tree.find('Цена').text + ' грн.' '</b>\n'

    item_foto = tree.find('АдресФотоНаСайте').text
    query_params = {'No': message.text}
    response = requests.get(f"{base_url_rest}/Items/Item_qty", auth=(username, password), verify=False,
                            params=query_params)

    soup = BeautifulSoup(response.text, 'lxml')
    rows = soup.find_all('row')

    mess = item_txt + '\n'
    for line in rows:
        shop_name = str(line.text).strip().split('\n')[0].ljust(30)
        qty = str(line.text).strip().split('\n')[1].rjust(3)
        mess += f"{shop_name}    {qty}" + '\n'

    bot.send_photo(message.chat.id, 'https://promenu.ua/' + item_foto)
    bot.send_message(message.chat.id, mess, parse_mode='html')

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти',
                                          url='https://promenu.ua/product-by-code1c/' + message.text))
    bot.send_message(message.chat.id, 'Сторінка товара на сайті', reply_markup=markup)


def find_by_dc_no(message):
    session = Session()
    session.verify = False
    session.auth = HTTPBasicAuth(username, password)
    transport = Transport(session=session)
    client = Client(base_url_soap + '_Clients?wsdl', transport=transport)
    # print(client.wsdl.dump())
    person = client.service.Get_clientShort(message.text, '', '')

    if person == 'empty':
        bot.send_message(message.chat.id, f'На жаль за номером картки: {message.text} - нікого не знайшли',
                         parse_mode='html')
        return

    soup = BeautifulSoup(person, 'lxml')

    person_txt = 'Ім''я: ' + '<b>' + soup.text.split('\n')[2] + '</b>\n' + \
                 'ДК: ' + '<b>' + soup.text.split('\n')[5] + '</b>\n' + \
                 'ББ: ' + '<b>' + soup.text.split('\n')[8] + '</b>\n'

    bot.send_message(message.chat.id, person_txt, parse_mode='html')
