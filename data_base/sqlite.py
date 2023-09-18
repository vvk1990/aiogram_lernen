import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('new.db')
    cur = db.cursor()


    cur.execute('''create table if not exists profile(user_id text primary key,
                                                  photo text,
                                                  age text,
                                                  description text,
                                                  name text)''')

    db.commit()

async def create_profile(user_id):
    user = cur.execute("select 1 from profile where user_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute('''insert into profile values(?, ?, ?, ?, ?)''', (user_id, '', '', '', ''))
        db.commit()

async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute('''update profile set photo = '{}', age = '{}', description ='{}', name = '{}' where user_id = '{}' '''
                            .format(data['photo'], data['age'], data['description'], data['name'], user_id))
        db.commit()