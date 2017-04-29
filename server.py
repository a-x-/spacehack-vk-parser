# -*- coding: utf-8 -*-

import vk_api
import json
import multiprocessing
from multiprocessing import Process, Value, Array
from time import sleep
from random import random

def get_wall(user_id, tools):
    """ Пример получения всех постов со стены """

    """ VkTools.get_all позволяет получить все объекты со всех страниц.
        Соответственно get_all используется только если метод принимает
        параметры: count и offset.
        Например может использоваться для получения всех постов стены,
        всех диалогов, всех сообщений, etc.
        При использовании get_all сокращается количество запросов к API
        за счет метода execute в 25 раз.
        Например за раз со стены можно получить 100 * 25 = 2500, где
        100 - максимальное количество постов, которое можно получить за один
        запрос (обычно написано на странице с описанием метода)
    """

    wall = tools.get_all('wall.get', 1000, {'owner_id': user_id})

    #print('Posts count:', wall['count'])
    return wall

def get_profile(user_id, vk_session, tools, f):
    #basic = api.users.get(user_ids=1, fields='photo,sex,bdate,city,country,education,relation,home_town,lists,personal,about')
    try:
        friends = tools.get_all('friends.get', 1000, {'user_id': user_id})
    except Exception as e:
        print(e)
        friends = None
    try:
        basic = vk_session.method('users.get', {'user_ids': user_id, 'fields': 'photo,sex,bdate,city,country,education,relation,home_town,lists,personal,about'})[0]
    except Exception as e:
        print(e)
        basic = None
    #basic.wall = api.wall(owner_id = user_id)
    try:
        wall = get_wall(user_id, tools)
    except Exception as e:
        print(e)
        wall = None
    f.write(json.dumps({'friends': friends, 'basic': basic, 'wall': wall, 'id': user_id, 'groups': None}, indent=4, ensure_ascii=False) + ',\n')

wide_last_id = 1000
deep_ids = []

def mp(wide_parse, deep_parse):
    parsers = []
    for cpu in range(0, multiprocessing.cpu_count()):
        parsers.append(Process(target=wide_parse, args=(Array('i', [wide_last_id]),)))
    #    parsers.append(Process(target=deep_parse, args=(Array('i', deep_ids),)))
    for parser in parsers:
        parser.start()
    for parser in parsers:
        parser.join()

def wide_parse(vk_session, tools, f):
    def fn (uid):
        while True:
            sleep(0.1 * random())
            uid[0] = uid[0] + 1
            get_profile(uid[0], vk_session, tools, f)

    return fn

def deep_parse():
    pass

def main():
    vk_session = vk_api.VkApi(token='b11913f3f200a5f61bf8cc2da28105f242a84714148f74452f5ec3c39c870fdf82b3e23da7fbe9f12f17f', app_id='6008096', client_secret='YBDSuGrvsC8vccTlenk8')

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)

    f = open('vk-users.json', 'a')
    f.write('[\n')

    #mp(wide_parse(vk_session, tools, f), deep_parse)
    for i in range(4015282, 40152820):
        get_profile(round(random() * 40152820 + 4005282), vk_session, tools, f)


if __name__ == '__main__':
    main()
