import psycopg2


def get_connection():
    return psycopg2.connect(database='database',
                            user='user',
                            password='password',
                            host='host',
                            port='port')


conn = get_connection()
cur = conn.cursor()
cur.execute("CREATE TABLE current_score (id serial PRIMARY KEY, point integer, bullet integer, created_at timestamp default CURRENT_TIMESTAMP);")
conn.commit()
cur.close()
conn.close()
