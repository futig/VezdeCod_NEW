import requests
from config import *
from time import sleep


def like_meme(meme_type: str, owner_id: int, item_id: int):
    response = requests.get('https://api.vk.com/method/likes.add',
                            params={
                                'access_token': token,
                                'v': API_VERSION,
                                'type': meme_type,
                                'owner_id': 0 - abs(owner_id),
                                'item_id': item_id
                            })


if __name__ == '__main__':
    like_meme("photo", 197700721, 457240646)