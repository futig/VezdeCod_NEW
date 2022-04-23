import requests
from config import token
from time import sleep

API_VERSION = 5.131


def get_user_name(user_id):
    response = requests.get('https://api.vk.com/method/users.get',
                            params={
                                'access_token': token,
                                'v': API_VERSION,
                                'user_ids': user_id
                            })
    return f"{response.json()['response'][0]['first_name']} {response.json()['response'][0]['last_name']}"



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
    print(1)
    sleep(0.1)
    print(2)