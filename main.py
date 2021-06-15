#!/usr/bin/env python3

from pydub import AudioSegment
import datetime
import speech_recognition as sr

from botmodules import *

if not path.exists(filename + '/img/'):
    makedirs(filename + '/img/')
if not path.exists(filename + '/data/'):
    makedirs(filename + '/data/')

try:
    sqlite_connection = sqlite3.connect('data/data.db')
    cursor = sqlite_connection.cursor()
    cursor.execute( '''CREATE TABLE blacklist (
                                id INT, 
                                name TEXT 
                                );''')
except Exception as err:
    print(err)
    with open(filename + '/data/log_bot.txt', "a") as f:
        f.write(str(datetime.datetime.now()) + ' ' + str(err) + '\n')
    pass
  
with open(filename + '/data/log.txt', "a") as f:
    f.write(str(datetime.datetime.now()) + '\n')

while True:
    r = sr.Recognizer()


    try:
        def main():
            try:
                for event in longpoll.listen():  # регистрируем событие
                    print("got event")
                    print(event.obj.peer_id)
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
                        send_photo(bot_api, event.obj.peer_id, *upload_photo(upload, reddit_photos(rnd, event.obj.peer_id), True, ''))
                        tier(event.obj.peer_id,event.object.from_id, search_list[-1])

                    elif event.type == VkBotEventType.MESSAGE_NEW and (search_list[-1] in settings['books']):
                        books(bot_api, event.obj.peer_id, settings['books'][search_list[-1]])
                    elif event.type == VkBotEventType.MESSAGE_NEW and (search_list[-1] =='detect'):
                        detect_public_ip(bot_api, event.obj.peer_id)

                    elif event.type == VkBotEventType.MESSAGE_NEW and ('booba' in search_list):
                        send_photo(bot_api, event.obj.peer_id,
                                   *upload_photo(upload, search_reddit('Italian Girl' + ' nsfw:1'), True,''))
                        tier(event.obj.peer_id,event.object.from_id, search_list[-1])

                    elif event.type == VkBotEventType.MESSAGE_NEW and 'search18' in search_list:
                        print(search_list[9:])
                        send_photo(bot_api, event.obj.peer_id,
                                   *upload_photo(upload, search_reddit(search_list[9:] + ' nsfw:1'), True,''))
                        tier(event.obj.peer_id,event.object.from_id, search_list[-1])

                    elif event.type == VkBotEventType.MESSAGE_NEW and 'search' in search_list:
                        send_photo(bot_api, event.obj.peer_id,
                                   *upload_photo(upload, search_reddit(search_list[7:] + ' nsfw:0'), True,''))
                        tier(event.obj.peer_id,event.object.from_id, search_list[-1])

            except Exception as err:
                print(err)
                with open(filename + '/data/log_bot.txt', "a") as f:
                    f.write(str(datetime.datetime.now())+' '+str(err) + '\n')
                pass

        if __name__ == '__main__':
            main()

    except requests.exceptions.ReadTimeout as timeout:
        continue
