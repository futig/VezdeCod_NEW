import sqlite3
import requests
from search_memes import *
from time import sleep
from actions import *

all_memes = []


# Заполняем таблицу
def fill_db(base, sql, album_owner_id=0, album_id=0, wall_owner_id=0, posts_amount=0):
    global all_memes
    if not album_owner_id == 0:
        all_memes = get_album_memes(owner_id=album_owner_id, album_id=album_id)
        if not wall_owner_id == 0:
            all_memes.extend(get_wall_memes(owner_id=wall_owner_id, posts_amount=posts_amount))
    elif not wall_owner_id == 0:
        all_memes = get_wall_memes(owner_id=wall_owner_id, posts_amount=posts_amount)
    elif wall_owner_id == 0 and album_owner_id == 0:
        raise "There aren't any memes to put in table"
    sleep(0.5)

    count = 0
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
        user_like = item['likes']['user_likes']
        likes = item['likes']['count']

        sql.execute("INSERT INTO vezdecod VALUES(?,?,?,?,?,?,?,?,?);",
                    (count, owner_id, user_name, item_id, item_type, likes, user_like, picture.content, picture_link))
        base.commit()
        sleep(0.15)
        count += 1


# Создаем базу данных
def create_base():
    base = sqlite3.connect("vezdecod.db")
    sql = base.cursor()
    sql.execute("DROP TABLE IF EXISTS vezdecod")
    base.commit()
    sql.execute("""CREATE TABLE IF NOT EXISTS vezdecod(
                id INTEGER PRIMARY KEY,
                owner_id INTEGER NOT NULL,
                user_name TEXT NOT NULL,
                item_id INTEGER NOT NULL,
                item_type TEXT NOT NULL,
                likes INTEGER NOT NULL,
                user_like INTEGER NOT NULL,
                picture BLOB NOT NULL,
                picture_link TEXT NOT NULL);
            """)
    base.commit()
    return base, sql


if __name__ == '__main__':
    db, cursor = create_base()
    try:
        fill_db(base=db, sql=cursor, album_owner_id=197700721, album_id=281940823, wall_owner_id=150550417, posts_amount=100)
        actions = Actions(cursor=cursor, selected_meme_id=457240646)
        next_meme = actions.like_meme(meme_type="photo", owner_id=197700721, item_id=457240646, user_like=0)
    # except Exception as e:
    #     print(e)
    finally:
        db.close()
    print('Task have been finished!')
