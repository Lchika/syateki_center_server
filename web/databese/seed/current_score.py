import psycopg2


def get_connection():
    return psycopg2.connect(database='syateki_center_server',
                            user='postgres',
                            password='admin',
                            host='localhost',
                            port='5432')


conn = get_connection()
cur = conn.cursor()
for i in range(10):
    cur.execute("INSERT INTO current_score (point, bullet) VALUES (%s, %s)", (0, 0))
conn.commit()
cur.close()
conn.close()
