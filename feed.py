from os import path, makedirs
from botmodules import *
import vk_api

from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll
import datetime

import yaml
import argparse

bot_session = vk_api.VkApi(
    token=settings['entertokens']['tokens'])
bot_api = bot_session.get_api()
upload = VkUpload(bot_session)
longpoll = VkBotLongPoll(bot_session, settings['entertokens']['group_id'])
keyboard = VkKeyboard(one_time=False)
keyboard.add_button(':tits', color=VkKeyboardColor.PRIMARY)
keyboard.add_button(':бушидо', color=VkKeyboardColor.PRIMARY)
keyboard.add_button(':сиси', color=VkKeyboardColor.PRIMARY)
keyboard.add_button(':Hello there', color=VkKeyboardColor.PRIMARY)


parser = argparse.ArgumentParser(description='настройки рассылки')
parser.add_argument('msgtext', type=str, help='текст сообщения')
parser.add_argument('peer_id', type=str, help='id группы')
args = parser.parse_args()
filename = getcwd()


with open(filename+'\settings.yaml', encoding='utf-8') as f:
    settings = yaml.safe_load(f)

if not path.exists(filename + '/img/'):
    makedirs(filename + '/img/')
if not path.exists(filename + '/log/'):
    makedirs(filename + '/log/')

with open(filename + '/log/log_bot.txt', "a") as f:
    f.write(str(datetime.datetime.now()) + '\n')

peer_id=2000000001

def main():
    rnd = random.choice(settings['dictionary']['tits_list'])
    print(rnd)
    #vk_msg_send(bot_api,peer_id,'check',False)
    send_photo(bot_api, args.peer_id, *upload_photo(upload, reddit_photos(str(rnd)),True,args.msgtext))
    print('send')



if __name__ == '__main__':
    main()



