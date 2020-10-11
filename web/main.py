from flask import Flask, request, render_template
import os
import urllib.request
import ssl
import re
import csv
import sys
import pathlib
import psycopg2
import json
parent_dir = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(parent_dir)
from common.c_debug import logger
from common.c_ping import Pings
from device.a_displayer import ApiDisplayer


config_type = {
    "development": "config.Development",
    "production": "config.Production",
    "testing": "config.Testing"
}


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config_type.get(os.getenv("FLASK_APP_ENV", "production")))
app.config.from_pyfile('config.cfg')


def targets_csv_path():
    return '/home/pi/syateki_center_server/web/targets.csv'


def set_target():
    hosts = []
    results = []
    for n in range(12):
        hosts.append("192.168.100." + str(200 + n))
    results = Pings().scan(hosts)
    ApiDisplayer().disp_connectivity(results)
    targets = []
    for i, r in enumerate(results):
        if r:
            targets.append("192.168.100." + str(200 + i))
    logger().info('targets = %s', targets)
    with open(targets_csv_path(), 'w') as f:
        writer = csv.writer(f)
        writer.writerow(targets)


def get_target_num(response):
    return re.search(r'(?<==)\d+', response).group()


def get_hit_num(targets, gun_num):
    ssl._create_default_https_context = ssl._create_unverified_context
    logger().info('targets = %s', targets)
    #if not targets:
    #    return (-1)
    for i, t in enumerate(targets):
        logger().info('connect to target: ' + str(i))
        # url_target = 'http://' + t
        url_target = 'http://' + t + '?gun_num=' + gun_num
        req = urllib.request.Request(url_target)
        target_num = '0'
        with urllib.request.urlopen(req) as res:
            res_html = res.read().decode('utf-8')
            # print('score_site res = ' + res_html)
            target_num = get_target_num(res_html)
            # logger().info('target_num = ' + target_num)
            if target_num == gun_num:
                logger().info('hit_num = ' + str(i + 1))
                return (i + 1)
    return (-1)


def get_connection():
    return psycopg2.connect(database=app.config['DB_NAME'],
                            user=app.config['DB_USER'],
                            password=app.config['DB_PASSWORD'],
                            host=app.config['DB_HOST'],
                            port=app.config['DB_PORT'])


def regist_score(time, score):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO scores (time, score) VALUES (%s, %s) RETURNING id", (time, score))
    id = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    logger().info('resisterd id = ' + str(id[0]))
    return id[0]


def get_rank(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT score_rank FROM (SELECT *, RANK() OVER(ORDER BY score DESC, time ASC) AS score_rank FROM scores) AS grade WHERE id = %s", (id,))
    rank = cur.fetchone()
    cur.execute("SELECT COUNT(id) FROM scores")
    cur.close()
    conn.close()
    logger().info('rank = ' + str(rank))
    return rank[0]


def get_records_num():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM scores")
    count = cur.fetchone()
    cur.close()
    conn.close()
    logger().info('rank = ' + str(count))
    return count[0]
# id = 1 ~ 10
@app.route("/shoot/<id>", methods=["GET"])
def get_shoot(id='1'):
    if request.method == "GET":
        targets = []
        with open(targets_csv_path()) as f:
            reader = csv.reader(f)
            targets = next(reader)
        hit_num = get_hit_num(targets, id)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE current_score SET bullet = bullet - 1 WHERE id = %s", (id,))
        if hit_num > 0:
            cur.execute("UPDATE current_score SET point = point + 1 WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return str(hit_num)

# id = 1 ~ 10
@app.route("/score/<id>", methods=["GET"])
def get_score(id='1'):
    if request.method == "GET":
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM current_score WHERE id = %s", (id,))
        score = cur.fetchone()
        cur.close()
        conn.close()
        dic = {'point': score[1], 'bullet': score[2]}
        return json.dumps(dic)


@app.route("/", methods=["GET"])
def root():
    player_num = request.args.get("player_num", 1)
    return render_template('index.html', player_num=int(player_num))


@app.route("/result", methods=["GET"])
def show_result():
    player_num = int(request.args.get("player_num", 1))
    scores = []
    for i in range(player_num):
        time = float(request.args.get("time" + str(i), -1.0))
        score = int(request.args.get("score" + str(i), -1))
        id = regist_score(time, score)
        rank = get_rank(id)
        scores.append({'time': time, 'score': score, 'rank': rank})
    count = get_records_num()
    return render_template('result.html', player_num=player_num, scores=scores, count=count)


@app.route("/init", methods=["GET"])
def init_score():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE current_score SET bullet = 20, point = 0")
    conn.commit()
    cur.close()
    conn.close()
    return "OK"


if __name__ == "__main__":
    #set_target()
    app.run("0.0.0.0")
