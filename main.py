#!/usr/bin/env python3

from pydub import AudioSegment
import speech_recognition as sr
from botmodules import *

'''
Проверяет существует ли ДБ и необхлодимые папки создает если нет
'''
if not path.exists(filename + '/img/'):
    makedirs(filename + '/img/')
if not path.exists(filename + '/data/'):
    makedirs(filename + '/data/')

try:
    sqlite_connection = sqlite3.connect('data/data.db')
    cursor = sqlite_connection.cursor()
    cursor.execute('''CREATE TABLE blacklist (
                                id INT, 
                                name TEXT 
                                );''')
except Exception as err:  # записываем ошибки в лог
    print(err)
    with open(filename + '/data/log_bot.txt', "a") as f:
        f.write(str(datetime.datetime.now()) + ' ' + str(err) + '\n')
    pass

with open(filename + '/data/log.txt', "a") as f:
    f.write(str(datetime.datetime.now()) + '\n')

while True:
    r = sr.Recognizer() # расспознователь аудио  в текст

    try:
        def main():
            try:
                for event in longpoll.listen():  # регистрируем событие
                    search_list = event.object['text'].lower().split(':')
                    try:
                        if event.object['attachments'][0]['type'] == 'audio_message':
                            '''
                            проверяем вляется ли сообщение аудио, если да дешифруем его
                            '''
                            wavv = requests.get(event.object['attachments'][0]['audio_message']['link_mp3']).content
                            sound = AudioSegment.from_mp3(BytesIO(wavv))
                            sound.export(filename + '/sound.wav', format="wav")
                            with sr.AudioFile(filename + '/sound.wav') as source:
                                audio = r.record(source)
                                search = (r.recognize_google(audio, language='ru-RU'))
                            search_list = search.lower().split(' ')
                    except:
                        pass
                    if event.type == VkBotEventType.MESSAGE_NEW and (search_list[-1] in settings['dictionary']):
                        '''
                        Если сообщение новое 
                        Проверяем наличие команды бота в словаре
                        '''
                        if type(settings['dictionary'][search_list[
                            -1]]) == list:  # если команда это список сообществ выбираем одно случайное
                            rnd = random.choice(settings['dictionary'][search_list[-1]])
                        else:
                            rnd = settings['dictionary'][search_list[-1]]
                        send_photo(bot_api, event.obj.peer_id,
                                   *upload_photo(upload, reddit_photos(rnd, event.obj.peer_id), True, ''))
                        tier(event.obj.peer_id, event.object.from_id, search_list[-1])  # запис в логи запроса

                    elif event.type == VkBotEventType.MESSAGE_NEW and (search_list[-1] in settings['books']):
                        books(bot_api, event.obj.peer_id, settings['books'][search_list[-1]])
                    elif event.type == VkBotEventType.MESSAGE_NEW and (search_list[-1] == 'detect'):
                        detect_public_ip(bot_api, event.obj.peer_id)

                    elif event.type == VkBotEventType.MESSAGE_NEW and 'search' in search_list:
                        '''
                         поиск по постам с выключенным nsfw 
                        '''
                        send_photo(bot_api, event.obj.peer_id,
                                   *upload_photo(upload, search_reddit(search_list[1] + ' nsfw:0', event.obj.peer_id),
                                                 True))
                        tier(event.obj.peer_id, event.object.from_id, search_list[-1])
                        '''
                         поиск по постам с включенным nsfw 
                        '''
                    elif event.type == VkBotEventType.MESSAGE_NEW and 'search18' in search_list:
                        send_photo(bot_api, event.obj.peer_id,
                                   *upload_photo(upload, search_reddit(search_list[1] + ' nsfw:1', event.obj.peer_id),
                                                 True))
                        tier(event.obj.peer_id, event.object.from_id, search_list[-1])
            except Exception as err: #  Запись ошибки в логи
                with open(filename + '/data/log_bot.txt', "a") as f:
                    f.write(str(datetime.datetime.now()) + ' ' + str(err) + '\n')
                pass


        if __name__ == '__main__':
            main()

    except requests.exceptions.ReadTimeout as timeout:
        continue
