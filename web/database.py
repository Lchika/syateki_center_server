import psycopg2


def get_connection():
    return psycopg2.connect(database='syateki_center_server',
                            user='postgres',
                            password='admin',
                            host='localhost',
                            port='5432')


conn = get_connection()
cur = conn.cursor()
cur.execute("CREATE TABLE current_score (id serial PRIMARY KEY, point integer, bullet integer, created_at timestamp default CURRENT_TIMESTAMP);")
conn.commit()
cur.close()
conn.close()
