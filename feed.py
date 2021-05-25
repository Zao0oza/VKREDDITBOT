from os import path, makedirs
from botmodules import *
import vk_api

from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll
import datetime

import argparse

bot_session = vk_api.VkApi(
    token=tokens['tokens'])
bot_api = bot_session.get_api()
upload = VkUpload(bot_session)
longpoll = VkBotLongPoll(bot_session, tokens['group_id'])
keyboard = VkKeyboard(one_time=False)
keyboard.add_button(':tits', color=VkKeyboardColor.PRIMARY)
keyboard.add_button(':бушидо', color=VkKeyboardColor.PRIMARY)
keyboard.add_button(':сиси', color=VkKeyboardColor.PRIMARY)
keyboard.add_button(':Hello there', color=VkKeyboardColor.PRIMARY)


parser = argparse.ArgumentParser(description='настройки рассылки')
parser.add_argument('--msg', type=str, help='текст сообщения', default='Вечер в хату')
parser.add_argument('--peer', type=str, help='id группы', default='2000000003')
args = parser.parse_args()
filename = getcwd()

if not path.exists(filename + '/img/'):
    makedirs(filename + '/img/')
if not path.exists(filename + 'data/'):
    makedirs(filename + 'data/')

with open(filename + '/data/log_bot.txt', "a") as f:
    f.write(str(datetime.datetime.now()) + '\n')

def main():
    rnd = random.choice(settings['dictionary']['feed'])
    send_photo(bot_api, args.peer, *upload_photo(upload, reddit_photos(str(rnd)), True, args.msg))
    print('send')

if __name__ == '__main__':
    main()



