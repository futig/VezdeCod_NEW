import requests
from config import token

API_VERSION = 5.131


# Получаем мемы из альбома Вездекод
def get_vezdecod_memes():
    album_id = '281940823'
    owner_id = '-197700721'
    response = requests.get('https://api.vk.com/method/photos.get',
                            params={
                                'access_token': token,
                                'v': API_VERSION,
                                'owner_id': owner_id,
                                'album_id': album_id,
                                'extended': 1
                            })
    return response.json()['response']['items']


# Получаем мемы со стены сообщества Reddit
def get_reddit_memes():
    owner_id = '-150550417'
    offset = 0
    all_posts = []
    while offset < 200:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': API_VERSION,
                                    'owner_id': owner_id,
                                    'count': 100,
                                    'offset': offset
                                })
        all_posts.extend(response.json()['response']['items'])
        offset += 100
    return all_posts


# Находит картинку лучшего качества
def find_best_picture(items):
    best_link = " "
    resolution = -1
    for link in items:
        if link['height'] > resolution:
            best_link = link['url']
            resolution = link['height']
    return best_link


# Находит имя пользователя по id
def get_user_name(user_id):
    response = requests.get('https://api.vk.com/method/users.get',
                            params={
                                'access_token': token,
                                'v': API_VERSION,
                                'user_ids': user_id
                            })
    try:
        return f"{response.json()['response'][0]['first_name']} {response.json()['response'][0]['last_name']}"
    except Exception:
        print(response.json())


# Находит имя группы по id
def get_group_name(owner_id):
    response = requests.get('https://api.vk.com/method/groups.getById',
                            params={
                                'access_token': token,
                                'v': API_VERSION,
                                'group_id': owner_id
                            })
    try:
        return response.json()['response'][0]['name']
    except Exception:
        print(response.json())


if __name__ == '__main__':
    pass