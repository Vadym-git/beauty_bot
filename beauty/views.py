from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from .models import Counties, BotUser, City
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
    counties = Counties.objects.all()
    keyboard = inline_keyboard(
        [[{'text': i.name.capitalize(), 'callback_data': f'*set_county,{i.id}'}] for i in counties])
    text = '&#129302; Супер! \n' \
           'Для початку, підкажи мені, в якому каунті(області) ти проживаєш, шукаєш послугу?\n'
    send_message(uid, text, parse_mode='HTML', reply_markup=keyboard)
    return


def set_county(uid, county):
    try:
        user = BotUser.objects.get(uid=uid)
        user.county = Counties.objects.get(pk=county)
        user.save()
        # if user.city:
        # text = 'Супер'
        # send_message(uid, )
    except:
        pass


bot_commands: dict = {
    '/start': start,
    '/go': go,
    '*set_county': set_county
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
    else:
        return 'Oops something went wrong'


def response_to_user_callback(uid, user_request: str):
    command, data = user_request.split(',')
    if command in bot_commands:
        command = bot_commands[command]
        command(uid, data)


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
