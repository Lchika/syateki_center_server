import psycopg2


def get_connection():
    return psycopg2.connect(database='database',
                            user='user',
                            password='password',
                            host='host',
                            port='port')


conn = get_connection()
cur = conn.cursor()
cur.execute("CREATE TABLE scores (id serial PRIMARY KEY, time real, miss integer default -1, score integer, name text default 'test', player_num integer default 0, created_at timestamp default CURRENT_TIMESTAMP);")
conn.commit()
cur.close()
conn.close()
