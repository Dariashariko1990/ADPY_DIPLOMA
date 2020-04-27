import psycopg2

con = psycopg2.connect("dbname=test user=test_owner password=1")
cur = con.cursor()

print("Database opened successfully")


# функция, которая создает таблицы
def create_db(name, columns):
    cur.execute("CREATE TABLE %s (%s);" % (name, columns))
    con.commit()
    print("Table created successfully")


name = 'users'
columns = 'id serial PRIMARY KEY, vk_id integer'
# create_db(name, columns)


name = 'users_matches'
columns = 'id serial PRIMARY KEY, user_id integer REFERENCES users(id), vk_url varchar(100)'
# create_db(name, columns)


name = 'matches_photos'
columns = 'id serial PRIMARY KEY, match_id integer REFERENCES users_matches(id), photo_url text'


# create_db(name, columns)

# функция, которая добавляет пользователя
def add_user(vk_id):
    cur.execute("insert into users (vk_id) values (%s) RETURNING id", (vk_id,))
    res = cur.fetchone()
    last_id = res[0]
    con.commit()
    print("User added successfully")
    return last_id


# функция, которая добавляет подошедшего пользоваеля (user_id - пользователь, вызывающий программу)
# используем результат (last_id), вернувшийся ф-цией add_user
def add_match(user_id, match_vk_url):
    cur.execute("insert into users_matches (user_id, vk_url) values (%s, %s) RETURNING id", (user_id, match_vk_url))
    res = cur.fetchone()
    last_id = res[0]
    con.commit()
    print("Matching user added successfully")
    return last_id


# last_id = add_user(20000000)
# print(last_id)


# match_id = add_match(last_id, 'https://vk.com/id34747001')


# функция, которая добавляет фотографии подошедшего пользоваеля (match_id - id подошедшего пользователя)
# используем результат (last_id), вернувшийся ф-цией add_match
def add_match_photos(match_id, photo_url):
    cur.execute("insert into matches_photos (match_id, photo_url) values (%s, %s) RETURNING id", (match_id, photo_url))
    res = cur.fetchone()
    #last_id = res[0]
    con.commit()
    print("Photo added successfully")
    #return last_id


# функция, выводящая всех подошедших пользователей и ссылки на фото
def get_user_matches(user_id):
    cur.execute(
        "SELECT users_matches.vk_url, matches_photos.photo_url FROM matches_photos join users_matches on users_matches.id = matches_photos.match_id join users on users.id = users_matches.user_id WHERE users.id = %s" % (
            user_id))
    # cur.execute("SELECT users_matches.vk_url, matches_photos.photo_url FROM matches_photos join users_matches on users_matches.id = matches_photos.match_id join users on users.id = users_matches.user_id")
    print(cur.fetchall())


# get_user_matches(5)


def write_db_output(account, output):
    last_id = add_user(account)
    for match in output:
        match_id = add_match(last_id, match['vk_link'])
        for photo in match['photos']:
            add_match_photos(match_id, photo)
