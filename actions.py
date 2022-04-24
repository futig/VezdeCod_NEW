import requests
from config import *


class Actions:
    def __init__(self, cursor, selected_meme_id):
        self.sql = cursor
        self.next_meme = 0
        self.selected_meme_id = selected_meme_id
        self.selected_meme = ()
        self.take_selected_meme()


    def like_meme(self, meme_type: str, owner_id: int, item_id: int):
        response = requests.get('https://api.vk.com/method/likes.add',
                                params={
                                    'access_token': token,
                                    'v': API_VERSION,
                                    'type': meme_type,
                                    'owner_id': 0 - owner_id,
                                    'item_id': item_id
                                })


    def skip_meme(self):
            pass


    # def createGenerator(self):
    #     for meme in self.all_memes:
    #         yield meme


    def take_selected_meme(self):
        self.sql.execute(f"SELECT * FROM vezdecod WHERE item_id = {self.selected_meme_id}")
        self.selected_meme = self.sql.fetchone()


    def print_data(self):
        self.sql.execute("SELECT * FROM vezdecod")
        for _, name, _, _, likes, _, picture_link in self.sql.fetchall():
            print(f"Author:{name} | Likes: {likes} | link: {picture_link}")