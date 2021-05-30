from vk_api.utils import get_random_id
import time
import re
from os import getcwd
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import sqlite3
from io import BytesIO
import yaml
import praw
filename = getcwd()

with open(filename+'/settings.yaml', encoding='utf-8') as f:
    settings = yaml.safe_load(f)
with open(filename+'/tokens.yaml', encoding='utf-8') as f:
    tokens = yaml.safe_load(f)

reddit = praw.Reddit(
    client_id=tokens['reddit_client_id'],
    client_secret=tokens['reddit_client_secret'],
    user_agent=tokens['reddit_user_agent']
)

keyboard = VkKeyboard(one_time=False)
keyboard.add_button(':tits', color=VkKeyboardColor.PRIMARY)
keyboard.add_button(':бушидо', color=VkKeyboardColor.PRIMARY)
keyboard.add_button(':сиси', color=VkKeyboardColor.PRIMARY)
keyboard.add_button(':Hello there', color=VkKeyboardColor.PRIMARY)
filename = getcwd()

def vk_msg_send(vk, peer_id, text, attachment):
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        attachment=attachment,
        keyboard=keyboard.get_keyboard(),
        message=text
    )

import requests

def detect_public_ip(vk, peer_id):
    try:
        # Use a get request for api.duckduckgo.com
        raw = requests.get('https://api.duckduckgo.com/?q=ip&format=json')
        # load the request as json, look for Answer.
        # split on spaces, find the 5th index ( as it starts at 0 ), which is the IP address
        answer = raw.json()["Answer"].split()[4]
    # if there are any connection issues, error out
    except Exception as e:
        return vk_msg_send(vk, peer_id, 'Error: {0}'.format(e), False)
    # otherwise, return answer
    else:
        vk_msg_send(vk, peer_id, answer, False)

def books(vk, peer_id, bookname):
    print('bush')
    string = random.choice(list(open(filename + '/data/' + bookname, encoding='utf-8')))
    vk_msg_send(vk, peer_id, string, False)


def is_image(url):  # проверяет является ли ссылка изображением
    for i in ['jpg', 'img', 'png']:
        if i[-3:] in url[-3:]:
            return True


def blacklist(url,peer_id):  # проверяет была ли уже такая ссылка
  
    url_list = load_database(peer_id)
    
    if url[9:] not in str(url_list):
        return True
    else:
        return False


def reddit_photos(subreddit_name,peer_id):  # получаем список с  постами сообщества
    adress_list = []
    i = 10
    while i != 0:
        for submission in reddit.subreddit(subreddit_name).hot(limit=i):
            print(submission.url)
            if is_image(submission.url):
                if blacklist(submission.url,peer_id):
                    adress_list.append([submission.url, submission.title, submission.permalink])
                    i = 0
                    break
                else:
                    i += 10
            else:
                i += 10
    return adress_list


def search_reddit(name):  # функция поиска на выходе список из 3-х эл-ов название поста url ссылка
    adress_list = []
    i = 10
    while i != 0:
        for submission in reddit.subreddit("all").search(name, sort='top', limit=i,
                                                         params={'include_over_18': 'on'}):
            if is_image(submission.url):
                if blacklist(submission.url):
                    adress_list.append([submission.url, submission.title, submission.permalink])
                    i = 0
                    break
                else:
                    i += 10
            else:
                i += 10
        if adress_list is not None and adress_list != []:
            print(adress_list)
            return adress_list
        else:
            return [['https://i.imgur.com/0uJilpc.jpg', '404', '404']]


def upload_photo(upload,
                 adress_list,
                 save,msgtext):  # загружает фото в оперативную память (адрес и название берется рандомно из списка)

    url, title, link = adress_list[0]
    img = requests.get(url).content
    f = BytesIO(img)
    try:
        response = upload.photo_messages(f)[0]
    except:
        img = requests.get(url).content
        f = BytesIO(img)
        response = upload.photo_messages(f)[0]
    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']
    return owner_id, photo_id, access_key, title, url, link, save, msgtext


def send_photo(vk, peer_id, owner_id, photo_id, access_key, title, url, link, save,msgtext):
    write_to_cheklist(url[9:],peer_id)
  # отправляет фото  в вк
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    text =msgtext+'\n' + str(title) + '\n' + 'https://www.reddit.com/' + str(link)
    vk_msg_send(vk, peer_id, text, attachment)
    if save is True:
        save_photo(url, title)


def save_photo(url, title):
    p = requests.get(url)
    out = open(filename + '/img/' + str(time.time()) + '-' + re.sub(r'[^aA-zZ]+', '', title) + url[-4::],
               "wb")
    out.write(p.content)
    out.close()


def write_to_cheklist(image, peer_id):  # записывает рандомно генерированные номера в txt
    temp_ = tuple([image])
    conn = sqlite3.connect(filename + "/data/data.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute('INSERT INTO blacklist (id,name) VALUES (?, ?)', (peer_id, image)) 
    conn.commit()


def load_database(peer_id):
    
    conn = sqlite3.connect(filename + "/data/data.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    sql = "SELECT name FROM blacklist where id ='%s'"% peer_id
    cursor.execute(sql)
    ("black")
    c=cursor.fetchall()
    return c


def tier(peer, id, search):
    with open(filename + '/data/tier.txt', "a") as f:
        f.write(str(peer) + ';' + str(id) + ';' + search + '\n')
