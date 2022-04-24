import sqlite3
import requests
from search_memes import *
from time import sleep
from actions import *

all_memes = []


# Заполняем таблицу
def fill_db(base, sql):
    global all_memes
    all_memes = get_album_memes(owner_id=197700721, album_id=281940823)
    all_memes.extend(get_wall_memes(owner_id=150550417, posts_amount=100))
    sleep(0.5)

    for item in all_memes:
        if len(item) > 13:
            try:
                if len(item['text']) > 100 or item['marked_as_ads'] == 1 or not len(item['attachments']) == 1 or not \
                        item['attachments'][0]['type'] == 'photo':
                    continue
            except Exception:
                print(item)

            picture_link = find_best_picture(item['attachments'][0]['photo']['sizes'])
            picture = requests.get(picture_link)
            item_type = "post"
            user_name = get_group_name_by_id(abs(item['owner_id']))
        else:
            picture_link = find_best_picture(item['sizes'])
            picture = requests.get(picture_link)
            item_type = "photo"
            user_name = get_user_name_by_id(item['user_id'])
        owner_id = item['owner_id']
        item_id = item['id']
        likes = item['likes']['count']

        sql.execute("INSERT INTO vezdecod VALUES(?,?,?,?,?,?,?);",
                    (owner_id, user_name, item_id, item_type, likes, picture.content, picture_link))
        base.commit()
        sleep(0.15)


# Создаем базу данных
def create_base():
    base = sqlite3.connect("vezdecod.db")
    sql = base.cursor()
    sql.execute("DROP TABLE IF EXISTS vezdecod")
    base.commit()
    sql.execute("""CREATE TABLE IF NOT EXISTS vezdecod(
                owner_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                item_id INTEGER NOT NULL,
                item_type TEXT NOT NULL,
                likes INTEGER NOT NULL,
                picture BLOB NOT NULL,
                picture_link TEXT NOT NULL);
            """)
    base.commit()
    return base, sql


if __name__ == '__main__':
    db, cursor = create_base()
    try:
        fill_db(db, cursor)
        actions = Actions(cursor, 457240646)
        actions.print_data()
    # except Exception as e:
    #     print(e)
    finally:
        db.close()
    print('Task have been finished!')
