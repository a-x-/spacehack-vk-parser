# -*- coding: utf-8 -*-

import vk_api
import json
from multiprocessing import Process, Value, Array

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

def get_profile(user_id, vk_session, tools):
    #basic = api.users.get(user_ids=1, fields='photo,sex,bdate,city,country,education,relation,home_town,lists,personal,about')
    basic = vk_session.method('users.get', {'user_ids': user_id, 'fields': 'photo,sex,bdate,city,country,education,relation,home_town,lists,personal,about'})
    #basic.wall = api.wall(owner_id = user_id)
    wall = get_wall(user_id, tools)
    print(json.dumps({'basic': basic, 'wall': wall}, indent=4, ensure_ascii=False))

wide_last_id = 1000
deep_ids = []

def mp(wide_parse, deep_parse):
    parsers = []
    for cpu in xrange(0, self.cores):
        parsers.append(Process(target=wide_parse, args=(Value('i', wide_last_id))))
        parsers.append(Process(target=deep_parse, args=(Array('i', deep_ids))))
    for parser in parsers:
        parser.start()
    for parser in parsers:
        parser.join()

def wide_parse():
    pass

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

    #mp(wide_parse, deep_parse)
    get_profile(1, vk_session, tools)


if __name__ == '__main__':
    main()
