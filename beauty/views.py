import time

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from .models import Counties, BotUser, City, BusinessField, ServiceType, Business
import requests

# Create your views here.

BOT = os.environ['bot_sk']
URL = fr"https://api.telegram.org/bot{BOT}/"


def start(uid, request):
    keyboard = reply_keyboard_markup([['/go'], ['/help']])
    text = 'Привіт &#129302;\n' \
           'Я файний бот який допоможе тобі, знайти послуги, які надають Українці котрі проживають в Ірландії\n' \
           '&#128269; Для початку пошуку натисни /go \n' \
           '&#128129;&#8205;&#9794;&#65039; Розмістити свої послуги, тисни: <a href="http://uado.ie">new_service</a>\n'
    send_message(uid, text, parse_mode='HTML', reply_markup=keyboard)
    return


def go(uid, request):
    text = '&#129302; Привіт! \n' \
           'Для початку, підкажи мені, в якому каунті(області) ти проживаєш, шукаєш послугу?\n'
    keyboard = inline_keyboard(
        [[{'text': '\U0001F301 Обрати свій county', 'callback_data': f'*get_counties,1'}],
         [{'text': '\U0001F4B1 Допомога / Help', 'callback_data': f'*help,1'}]],
    )
    send_message(uid, text, parse_mode='HTML', reply_markup=keyboard)
    return


def get_service_contacts(uid, request):
    contacts = Business.objects.get(id=request)
    wrong = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', ' -', '=', '|', '{', '}', '.', '!']
    insta = contacts.insta
    telegram = contacts.telegram
    email = contacts.email
    phone = contacts.phone
    for symbol in wrong:
        insta = insta.replace(symbol, '\\' + symbol)
        telegram = telegram.replace(symbol, '\\' + symbol)
        email = email.replace(symbol, '\\' + symbol)
        phone = phone.replace(symbol, '\\' + symbol)
    text = f'*\u2705 {contacts.name.capitalize()}*\n'
    text = text + f'{contacts.about[:4000]}\n' if contacts.about else text
    text = text + f'instagram\.com/{insta}\n' if contacts.insta and contacts.insta != 'none' else text
    text = text + f'email: {email}\n' if contacts.email else text
    text = text + f'telegram: {telegram}\n' if contacts.telegram else text
    text = text + f'phone: {phone}\n' if contacts.phone else text
    keyboard = inline_keyboard(
        [
            [{'text': '\U0001F4B1 ^ Всі послуги ^', 'callback_data': f'*get_service_services,{contacts.id}'}],
            [{'text': '\U0001F485 Пошук у моєму місті', 'callback_data': f'*city_services,1'}],
            [{'text': '\U0001F9D1\u200D\U0001F33E Пошук у моєму county', 'callback_data': f'*county_services,1'}],
            [{'text': '\U0001F4B1 Допомога / Help', 'callback_data': f'*help,1'}],
        ]
    )
    send_message(uid, text, parse_mode='MarkdownV2', reply_markup=keyboard)


def get_service_services(uid, request):
    try:
        service = Business.objects.get(id=request)
        services = service.servicetype_set.all()
        text = f'*{service.name.capitalize()}*\n'
        wrong = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', ' -', '=', '|', '{', '}', '.', '!']
        if len(services) == 0:
            keyboard = inline_keyboard(
                [
                    [{'text': '\U0001F4E8 ^ Всі контакти ^', 'callback_data': f'*get_service_contacts,{service.id}'}],
                    [{'text': '\U0001F4B1 Допомога / Help', 'callback_data': f'*help,1'}],
                ]
            )
            text = f'Здається нічого не було додано \U0001F628'
            send_message(uid, text, reply_markup=keyboard)
        for n in services:
            name = n.name[:32]
            price = str(n.price)
            for symbol in wrong:
                name = name.replace(symbol, '\\' + symbol)
                price = price.replace(symbol, '\\' + symbol)
            text = text + f'Service: {name}\n'
            text = text + f'Price: €{price}'
            keyboard = inline_keyboard(
                [[{'text': '\U0001F4E8 ^ Всі контакти ^', 'callback_data': f'*get_service_contacts,{service.id}'}],
                 [{'text': '\U0001F4B1 Допомога / Help', 'callback_data': f'*help,1'}],
                 ]
            )
            send_message(uid, text, parse_mode='MarkdownV2', reply_markup=keyboard)
            time.sleep(0.3)
    except Exception as es:
        pass


def county_services(uid, request):
    try:
        user = BotUser.objects.get(uid=uid)
        services = Business.objects.filter(county_id=user.county_id).filter(type_of_business=user.business_field)
        wrong = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', ' -', '=', '|', '{', '}', '.', '!']
        if len(services) == 0:
            keyboard = inline_keyboard(
                [[{'text': '\U0001F4B1 Допомога / Help', 'callback_data': f'*help,1'}]]
            )
            text = 'Здається нічого не знайдено \U0001F628'
            send_message(uid, text, reply_markup=keyboard)
        for service in services:
            insta = service.insta
            telegram = service.telegram
            email = service.email
            for symbol in wrong:
                insta = insta.replace(symbol, '\\' + symbol)
                telegram = telegram.replace(symbol, '\\' + symbol)
                email = email.replace(symbol, '\\' + symbol)
            text = f'*\u2705 {service.name.capitalize()}*\n'
            text = text + f'{service.about[:4000]}\n' if service.about else text
            text = text + f'instagram\.com/{insta}\n' if service.insta and service.insta != 'none' else text
            text = text + fr'email: ||{email}||' if service.email else text
            keyboard = inline_keyboard(
                [[{'text': '\U0001F4B1 ^ Всі послуги ^', 'callback_data': f'*get_service_services,{service.id}'},
                  {'text': '\U0001F4E8 ^ Всі контакти ^', 'callback_data': f'*get_service_contacts,{service.id}'}],
                 [{'text': '\U0001F4B1 Допомога / Help', 'callback_data': f'*help,1'}],
                 ]
            )
            send_message(uid, text, parse_mode='MarkdownV2', reply_markup=keyboard)
            time.sleep(0.3)
    except Exception as es:
        pass


def city_services(uid, request):
    user = BotUser.objects.get(uid=uid)
    services = Business.objects.filter(city_id=user.city_id).filter(type_of_business=user.business_field)
    wrong = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', ' -', '=', '|', '{', '}', '.', '!']
    if len(services) == 0:
        keyboard = inline_keyboard(
            [[{'text': '\U0001F4B1 Допомога / Help', 'callback_data': f'*help,1'}]]
        )
        text = 'Здається нічого не знайдено \U0001F628'
        send_message(uid, text, reply_markup=keyboard)
    for service in services:
        insta = service.insta
        telegram = service.telegram
        email = service.email
        for symbol in wrong:
            insta = insta.replace(symbol, '\\' + symbol)
            telegram = telegram.replace(symbol, '\\' + symbol)
            email = email.replace(symbol, '\\' + symbol)
        text = f'*{service.name.capitalize()}*\n'
        text = text + f'{service.about[:4000]}\n' if service.about else text
        text = text + f'instagram\.com/{insta}\n' if service.insta and service.insta != 'none' else text
        text = text + fr'email: ||{email}||' if service.email else text
        keyboard = inline_keyboard(
            [[{'text': '\U0001F4B1 ^ Всі послуги ^', 'callback_data': f'*get_service_services,{service.id}'},
              {'text': '\U0001F4E8 ^ Всі контакти ^', 'callback_data': f'*get_service_contacts,{service.id}'}],
             [{'text': '\U0001F4B1 Допомога / Help', 'callback_data': f'*help,1'}]
             ]
        )
        send_message(uid, text, parse_mode='MarkdownV2', reply_markup=keyboard)
        time.sleep(0.3)


def set_business_field(uid, business_field_id):
    try:
        text = '\U0001F917 Все налаштовано!\n' \
               '\U0001F50DТепер ти можеш розпочати прошук\n' \
               'Переглянути всі послуги в твоєму місті /city_services\n' \
               'Переглянути всі послуги в твоєму county /county_services\n'
        user = BotUser.objects.get(uid=uid)
        user.business_field_id = business_field_id
        user.save()
        keyboard = inline_keyboard(
            [[{'text': '\U0001F485 Пошук у моєму місті', 'callback_data': f'*city_services,1'}],
             [{'text': '\U0001F9D1\u200D\U0001F33E Пошук у моєму county', 'callback_data': f'*county_services,1'}],
             [{'text': '\U0001F4B1 Допомога / Help', 'callback_data': f'*help,1'}]
             ]
        )
        send_message(uid, text, reply_markup=keyboard)
    except Exception as es:
        print(es, '!' * 100)


def get_business_fields(uid, request):
    services = BusinessField.objects.all()
    text = '\U0001F60E Оберіть сфуре послуг нижче'
    keyboard = inline_keyboard(
        [[{'text': i.name.capitalize(), 'callback_data': f'*set_business_field,{i.id}'}] for i in services]
    )
    send_message(uid, text, reply_markup=keyboard)


def set_city(uid, city_id):
    try:
        user = BotUser.objects.get(uid=uid)
        user.city_id = city_id
        user.save()
        keyword = inline_keyboard(
            [[{'text': '\U0001F481 Обрати сферу послуг', 'callback_data': f'*get_business_fields,1'}]]
        )
        text = '&#129302; Просто чудово\n' \
               'Залишився останній крок - обрати сферу послуг!\n' \
               'Тисни "Обрати сферу послуг"\n'
        send_message(uid, text, reply_markup=keyword)
    except BotUser.DoesNotExist:
        print('set_city, something wrong', '!' * 100)


def get_cities(uid, county_id):
    try:
        cities = City.objects.filter(county=county_id)
        keyboard = inline_keyboard(
            [[{'text': i.name.capitalize(), 'callback_data': f'*set_city,{i.id}'}] for i in cities])
        text = '&#129302; Будь ласка, виберіть ваше місто зі списку нижче:'
        send_message(uid, text, reply_markup=keyboard)
    except ValueError:
        keyboard = inline_keyboard(
            [[{'text': 'Вибрати каунті', 'callback_data': f'*get_counties,1'}],
             [{'text': '\U0001F4B1 Допомога / Help', 'callback_data': f'*help,1'}]
             ])
        text = '&#129302; Здається ти не обрав каунті:'
        send_message(uid, text, reply_markup=keyboard)


def set_county(uid, county):
    try:
        user = BotUser.objects.get(uid=uid)
        user.county_id = county
        user.city_id = None
        user.save()
        text = 'Супер &#128076;\nЯ додав налаштування county до твого профілю!\n' \
               'Щоб налаштувати місто, для пошуку тисни\n"&#127961;&#65039; Налаштувати місто"'
        keyboard = inline_keyboard(
            [[{'text': '\U0001F3D9 Налаштувати місто', 'callback_data': f'*get_cities,{county}'}]])
        send_message(uid, text, reply_markup=keyboard)
    except:
        pass


def get_counties(uid, request):
    counties = Counties.objects.all()
    text = '\U0001FA90 Вибери свій county зі списку нижче'
    keyboard = inline_keyboard(
        [[{'text': i.name.capitalize(), 'callback_data': f'*set_county,{i.id}'}] for i in counties]
    )
    send_message(uid, text, parse_mode='HTML', reply_markup=keyboard)


def user_settings(uid, request):
    user = BotUser.objects.get(uid=uid)
    text = f'County: {user.county}\n' \
           f'City: {user.city}\n' \
           f'Service type: {user.business_field}\n'
    keyboard = inline_keyboard(
        [[{'text': '\U0001F4B1 Допомога / Help', 'callback_data': f'*help,1'}]]
    )
    send_message(uid, text, reply_markup=keyboard)


def help(uid, request):
    text = "Привіт!\n" \
           "Я \U0001F412 працюю у тестовому режимі, зважай на це!\n" \
           "змінити каунті: /get_counties\n" \
           "змінити місто: /get_cities\n" \
           "змінити сферу послуг: /get_business_fields\n" \
           "пошук в моєму місті: /city_services\n" \
           "пошук в моєму каунті: /county_services\n" \
           "налаштувати все зановго: /go\n" \
           'Розмістити послугу: <a href="http://www.uado.ie/">НАТИСНИ НА МЕНЕ</a>\n' \
           "Мої налаштування: /my_settings"

    send_message(uid, text, parse_mode='HTML')


bot_commands: dict = {
    '/start': start,
    '/go': go,
    '*set_county': set_county,
    '*get_cities': get_cities,
    '/get_cities': get_cities,
    '*set_city': set_city,
    '*get_business_fields': get_business_fields,
    '/get_business_fields': get_business_fields,
    '*set_business_field': set_business_field,
    '*get_counties': get_counties,
    '/get_counties': get_counties,
    '/county_services': county_services,
    '*county_services': county_services,
    '/city_services': city_services,
    '*city_services': city_services,
    '*get_service_contacts': get_service_contacts,
    '*get_service_services': get_service_services,
    '/help': help,
    '*help': help,
    '*my_settings': user_settings,
    '/my_settings': user_settings,
}


def reply_keyboard_markup(keyboard: list):
    return json.dumps({"keyboard": keyboard, "one_time_keyboard": True, 'resize_keyboard': True})


def inline_keyboard(keyboard):
    reply_markup = {"inline_keyboard": keyboard}
    return json.dumps(reply_markup)


def response_to_user_request(uid, user_request: str):
    if user_request in bot_commands:
        command = bot_commands[user_request]
        return command(uid, user_request)
    elif user_request[0] == '!':
        send_message(uid, 'Oops')
    else:
        send_message(uid, '&#129302; Хм, я не розумію, що ти від мене хочеш.')


def response_to_user_callback(uid, user_request: str):
    command, data = user_request.split(',')
    if command in bot_commands:
        command = bot_commands[command]
        command(uid, data)
    else:
        print(f'command: {command} not in bot_commands', '#' * 45)


def send_message(uid, text: str, parse_mode='HTML', reply_markup='', url: str = 'sendMessage'):
    headers = {
        'chat_id': uid,
        'text': text,
        'parse_mode': parse_mode,
        'reply_markup': reply_markup if reply_markup else ''
    }
    try:
        response = requests.post(URL + url, json=headers)
        # print(response.content)
    except Exception as es:
        exit(es)


def send_callbackquery(cid, text, alert: bool = True, url: str = ''):
    headers = {
        'callback_query_id': cid,
        'text': text,
        'show_alert': alert,
        'URL': url
    }
    try:
        response = requests.post(URL + 'answerCallbackQuery', json=headers)
    except Exception as es:
        exit(es)


def parse_request(request: dict):
    message = request.get('message')
    callback_query = request.get('callback_query')
    if callback_query:
        cid = callback_query.get('id')
        user_request = callback_query.get('data')
        uid = BotUser.check_registration(callback_query.get('from'))  # check registration in db
        send_callbackquery(cid, 'Success', False)
        response_to_user_callback(uid, user_request)
    if message:
        uid = BotUser.check_registration(message.get('from'))  # check registration in db
        user_request = message.get('text')
        if user_request:
            response_to_user_request(uid, user_request)
        else:
            send_message(uid, 'Упс &#129322, тут якась праблємка - щось пішло не так!')


@csrf_exempt
def index(request):  # get request
    request = json.loads(request.body)
    parse_request(request)
    return HttpResponse(status=200)
