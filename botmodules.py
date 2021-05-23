from vk_api.utils import get_random_id
import time
import re
from os import getcwd
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import requests
from io import BytesIO
import yaml
import praw
filename = getcwd()

with open(filename+'\settings.yaml', encoding='utf-8') as f:
    settings = yaml.safe_load(f)

reddit = praw.Reddit(
    client_id=settings['entertokens']['reddit_client_id'],
    client_secret=settings['entertokens']['reddit_client_secret'],
    user_agent=settings['entertokens']['reddit_user_agent']
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


def bushdo(vk, peer_id):
    print('bush')
    string = random.choice(list(open(filename + '/log/bushido2.txt')))
    vk_msg_send(vk, peer_id, string, False)


def is_image(url):  # проверяет является ли ссылка изображением
    for i in ['jpg', 'img', 'png']:
        if i[-3:] in url[-3:]:
            return True


def blacklist(url):  # проверяет была ли уже такая ссылка
    try:
        url_list = list(open(filename + '/log/blacklist.txt'))
    except:
        url_list = ['']
    if url[9:] not in str(url_list):
        return True
    else:
        return False


def reddit_photos(subreddit_name):  # получаем список с  постами сообщества
    adress_list = []
    i = 10
    while i != 0:
        for submission in reddit.subreddit(subreddit_name).hot(limit=i):
            if is_image(submission.url):
                if blacklist(submission.url):
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
        if adress_list is not None:
            return adress_list


def upload_photo(upload,
                 adress_list,
                 save,msgtext):  # загружает фото в оперативную память (адрес и название берется рандомно из списка)

    url, title, link = adress_list[0]
    write_to_cheklist(url[9:])
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


def send_photo(vk, peer_id, owner_id, photo_id, access_key, title, url, link, save,msgtext):  # отправляет фото  в вк
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


def write_to_cheklist(i):  # записывает рандомно генерированные номера в txt
    temp_ = tuple([i])
    with open(filename + '/log/blacklist.txt', "a") as f:
        f.write(str(temp_) + '\n')


def tier(peer, id, search):
    with open(filename + '/log/tier.txt', "a") as f:
        f.write(str(peer) + ';' + str(id) + ';' + search + '\n')
