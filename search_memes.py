import requests
from config import token

API_VERSION = 5.131


# Возвращает мемы из указанного альбома в формате json
# owner_id - id сообщества (записывается с минусом вначале '-124631533')
# album_id - id альбома в сообществе
def get_album_memes(owner_id: int, album_id: int):
    # album_id = '281940823'
    # owner_id = '-197700721'
    response = requests.get('https://api.vk.com/method/photos.get',
                            params={
                                'access_token': token,
                                'v': API_VERSION,
                                'owner_id': owner_id,
                                'album_id': album_id,
                                'extended': 1
                            })
    return response.json()['response']['items']


# Возвращает мемы со стены указанного сообщества в формате json
# owner_id - id сообщества (записывается С МИНУСОМ вначале '-124631533')
# posts_amount - кол-во взятых постов
def get_wall_memes(owner_id: int, posts_amount: int):
    # owner_id = -150550417
    count = 100 if posts_amount >= 100 else posts_amount
    watched_posts = 0
    offset = 0
    all_posts = []

    while posts_amount > watched_posts:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': API_VERSION,
                                    'owner_id': owner_id,
                                    'count': count,
                                    'offset': offset
                                })
        all_posts.extend(response.json()['response']['items'])
        offset += 100
        watched_posts += count
        count = posts_amount - watched_posts
    return all_posts


# Находит картинку лучшего качества среди предложенных
# Получает на вход json путь к фотографиям до 'sizes' (item['attachments'][0]['photo']['sizes'])
def find_best_picture(items):
    best_link = " "
    resolution = -1
    for link in items:
        if link['height'] > resolution:
            best_link = link['url']
            resolution = link['height']
    return best_link


# Находит имя пользователя по id
def get_user_name_by_id(user_id):
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
# owner_id - id сообщества (записывается БЕЗ минуса вначале '124631533')
def get_group_name_by_id(owner_id):
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