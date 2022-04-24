import requests
from config import *
import random


class Actions:
    # Принимает курсор и id выбранного мема для жульничества
    def __init__(self, cursor, selected_meme_id):
        self.sql = cursor
        self.next_meme = 1
        self.selected_meme_id = selected_meme_id
        self.selected_meme = ()
        self.take_selected_meme()

    # Лайкает мем от имени пользователя
    def like_meme(self, meme_type: str, owner_id: int, item_id: int, user_like: int):
        response = requests.get('https://api.vk.com/method/likes.add',
                                params={
                                    'access_token': token,
                                    'v': API_VERSION,
                                    'type': meme_type,
                                    'owner_id': 0 - abs(owner_id),
                                    'item_id': item_id
                                })
        if user_like == 0:
            self.sql.execute(f"SELECT * FROM vezdecod WHERE item_id = {item_id}")
            _, _, _, _, _, likes, _, _, _ = self.sql.fetchone()
            self.sql.execute(f"UPDATE vezdecod SET likes = {likes + 1} WHERE item_id = {item_id}")
        return self.skip_meme()

    # Пропускает мем
    def skip_meme(self):
        choice = 1 if random.random() > 0.17 else 0
        if choice:
            self.sql.execute(f"SELECT * FROM vezdecod WHERE id = {self.next_meme}")
            self.next_meme += 1
            return self.sql.fetchone()
        else:
            return self.selected_meme

    # Находит информацию о выбранном меме для жульничества в базе
    def take_selected_meme(self):
        self.sql.execute(f"SELECT * FROM vezdecod WHERE item_id = {self.selected_meme_id}")
        self.selected_meme = self.sql.fetchone()

    # Выводит информацию о мемах
    def print_data(self):
        self.sql.execute("SELECT * FROM vezdecod")
        for _, _, name, _, _, likes, _, _, picture_link in self.sql.fetchall():
            print(f"Author: {name} | Likes: {likes} | link: {picture_link}")
