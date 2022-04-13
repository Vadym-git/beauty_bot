from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from .models import Counties, BotUser, City, BusinessField, ServiceType
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
        [[{'text': '\U0001F301 Обрати свій county', 'callback_data': f'*get_counties,1'}]]
    )
    send_message(uid, text, parse_mode='HTML', reply_markup=keyboard)
    return


def county_services(uid, request):
    user = BotUser.objects.get(uid=uid)
    services = ServiceType.objects.filter(owner__county_id=user.county_id).filter(
        owner__type_of_business_id=user.business_field)


def set_business_field(uid, business_field_id):
    try:
        text = '\U0001F917 Все налаштовано!\n' \
               'Тепер ти можеш розпочати прошук \U0001F50D \n' \
               'Або переглянути всі послуги в твоєму місті, чи county\n' \
               'Для пошуку просто відправ мені свій запит та не забудь вказати перед ним знак оклику "!"\n' \
               'До прикладу:\n' \
               '!жіноча стрижка\n' \
               '!манікюр\n'
        user = BotUser.objects.get(uid=uid)
        user.business_field_id = business_field_id
        user.save()
        send_message(uid, text)
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
    cities = City.objects.filter(county=county_id)
    keyboard = inline_keyboard(
        [[{'text': i.name.capitalize(), 'callback_data': f'*set_city,{i.id}'}] for i in cities])
    text = '&#129302; Будь ласка, виберіть ваше місто зі списку нижче:'
    send_message(uid, text, reply_markup=keyboard)


def set_county(uid, county):
    try:
        user = BotUser.objects.get(uid=uid)
        user.county_id = county
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


bot_commands: dict = {
    '/start': start,
    '/go': go,
    '*set_county': set_county,
    '*get_cities': get_cities,
    '*set_city': set_city,
    '*get_business_fields': get_business_fields,
    '*set_business_field': set_business_field,
    '*get_counties': get_counties,
    '/county_services': county_services,
    # '/help': '',
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
