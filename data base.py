import sqlite3
from search_memes import *
from time import sleep

all_memes = []


def create_db():
    global all_memes
    # Создаем базу данных
    db = sqlite3.connect("vezdecod.db")
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS vezdecod(
        owner_id INTEGER,
        user_name TEXT,
        item_id INTEGER,
        item_type TEXT,
        likes INTEGER,
        picture_link TEXT);
    """)
    db.commit()

    all_memes = get_vezdecod_memes()
    all_memes.extend(get_reddit_memes())
    sleep(0.5)

    # Заполняем таблицу
    try:
        for item in all_memes:
            if len(item) > 13:
                try:
                    if len(item['text']) > 100 or item['marked_as_ads'] == 1 or not len(item['attachments']) == 1 or not item['attachments'][0]['type'] == 'photo':
                        continue
                except Exception:
                    print(item)

                picture_link = find_best_picture(item['attachments'][0]['photo']['sizes'])
                item_type = "post"
                user_name = get_group_name(abs(item['owner_id']))
            else:
                picture_link = find_best_picture(item['sizes'])
                item_type = "photo"
                user_name = get_user_name(item['user_id'])
            owner_id = item['owner_id']
            item_id = item['id']
            likes = item['likes']['count']

            cursor.execute("INSERT INTO vezdecod VALUES(?,?,?,?,?,?);", (owner_id, user_name, item_id, item_type, likes, picture_link))
            db.commit()
            sleep(0.15)
    finally:
        db.close()


if __name__ == '__main__':
    create_db()
    print(0)