import sqlite3
from search_memes import *
from time import sleep

all_memes = []


# Заполняем таблицу
def fill_db(base, sql):
    global all_memes
    all_memes = get_album_memes(owner_id=-197700721, album_id=281940823)
    all_memes.extend(get_wall_memes(owner_id=-150550417, posts_amount=100))
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
            item_type = "post"
            user_name = get_group_name_by_id(abs(item['owner_id']))
        else:
            picture_link = find_best_picture(item['sizes'])
            item_type = "photo"
            user_name = get_user_name_by_id(item['user_id'])
        owner_id = item['owner_id']
        item_id = item['id']
        likes = item['likes']['count']

        sql.execute("INSERT INTO vezdecod VALUES(?,?,?,?,?,?);",
                    (owner_id, user_name, item_id, item_type, likes, picture_link))
        base.commit()
        sleep(0.15)


if __name__ == '__main__':
    # Создаем базу данных
    db = sqlite3.connect("vezdecod.db")
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS vezdecod(
            owner_id INTEGER,
            user_name TEXT,
            item_id INTEGER primary key,
            item_type TEXT,
            likes INTEGER,
            picture_link TEXT);
        """)
    db.commit()
    try:
        fill_db(db, cursor)

    except Exception as e:
        print(e)
    finally:
        db.close()
    print('Task have been finished!')
