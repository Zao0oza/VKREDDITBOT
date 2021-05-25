#!/usr/bin/env python3

from pydub import AudioSegment
from os import path, makedirs
import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import datetime
import speech_recognition as sr

from botmodules import *

if not path.exists(filename + '/img/'):
    makedirs(filename + '/img/')
if not path.exists(filename + '/data/'):
    makedirs(filename + '/data/')

with open(filename + '/data/log.txt', "a") as f:
    f.write(str(datetime.datetime.now()) + '\n')
    
def new_event(event):
	search_list = event.object['text'].lower().split(':')
	try:
	                           if event.object['attachments'][0]['type'] == 'audio_message':
                            wavv = requests.get(event.object['attachments'][0]['audio_message']['link_mp3']).content
                            sound = AudioSegment.from_mp3(BytesIO(wavv))
                            sound.export(filename + '/sound.wav', format="wav")
                            with sr.AudioFile(filename + '/sound.wav') as source:
                                audio = r.record(source)
                                search = (r.recognize_google(audio, language='ru-RU'))
                            search_list = search.lower().split(' ')
                            print(search_list)
                    except:
                        print('no')

                    if event.type == VkBotEventType.MESSAGE_NEW and (search_list[-1] in settings['dictionary']):
                        if type(settings['dictionary'][search_list[-1]]) == list :
                            rnd = random.choice(settings['dictionary'][search_list[-1]])
                        else:
                            rnd = settings['dictionary'][search_list[-1]]
                        send_photo(bot_api, event.obj.peer_id, *upload_photo(upload, reddit_photos(str(rnd)), True, ''))
                        send_photo(bot_api, event.obj.peer_id,
                                   *upload_photo(upload, reddit_photos(settings['dictionary'][search_list[-1]]), True,''))
                        tier(event.obj.peer_id,event.object.from_id, search_list[-1])

                    elif event.type == VkBotEventType.MESSAGE_NEW and (search_list[-1] in settings['books']):
                        books(bot_api, event.obj.peer_id, settings['books'][search_list[-1]])

                    elif event.type == VkBotEventType.MESSAGE_NEW and ('booba' in search_list):
                        send_photo(bot_api, event.obj.peer_id,
                                   *upload_photo(upload, search_reddit('Italian Girl' + ' nsfw:1'), True,''))
                        tier(event.obj.peer_id,event.object.from_id, search_list[-1])

                    elif event.type == VkBotEventType.MESSAGE_NEW and 'search' in search_list:
                        send_photo(bot_api, event.obj.peer_id,
                                   *upload_photo(upload, search_reddit(search_list[1] + ' nsfw:0'), True,''))
                        tier(event.obj.peer_id,event.object.from_id, search_list[-1])

                    elif event.type == VkBotEventType.MESSAGE_NEW and 'search18' in search_list:
                        send_photo(bot_api, event.obj.peer_id,
                                   *upload_photo(upload, search_reddit(search_list[1] + ' nsfw:1'), True,''))
                        tier(event.obj.peer_id,event.object.from_id, search_list[-1])
while True:
    r = sr.Recognizer()
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

    try:
        def main():
            try:
                for event in longpoll.listen():  # регистрируем событие
                    print("got event")
                    print(event.obj.peer_id
                    event_new(event)


            except Exception as err:
                print(err)
                with open(filename + '/data/log_bot.txt', "a") as f:
                    f.write(str(datetime.datetime.now())+' '+str(err) + '\n')
                pass

        if __name__ == '__main__':
            main()

    except requests.exceptions.ReadTimeout as timeout:
        continue
