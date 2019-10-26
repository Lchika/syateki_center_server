from flask import Flask, request
import urllib.request
import ssl
import re
import sys
import pathlib
parent_dir = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(parent_dir)
from common.c_debug import logger
from common.c_ping import Pings


app = Flask(__name__)
pings = Pings()
__targets = []


def set_target():
    hosts = []
    results = []
    for n in range(12):
        hosts.append("192.168.100." + str(200 + n))
    results = pings.scan(hosts)
    __targets = []
    for i, r in enumerate(results):
        if r:
            __targets.append("192.168.100." + str(200 + i))
    logger().info('targets = %s', __targets)


def get_target_num(response):
    return re.search(r'(?<==)\d+', response).group()


def get_hit_num(targets, gun_num):
    ssl._create_default_https_context = ssl._create_unverified_context
    for i, t in enumerate(targets):
        url_target = 'http://' + t
        req = urllib.request.Request(url_target)
        target_num = '0'
        with urllib.request.urlopen(req) as res:
            res_html = res.read().decode('utf-8')
            # print('score_site res = ' + res_html)
            target_num = get_target_num(res_html)
            if target_num == gun_num:
                return i
            # print('target_num = ' + target_num)
    return (-1)


@app.route("/shoot/1", methods=["GET"])
def get_shoot():
    if request.method == "GET":
        return str(get_hit_num(__targets, '1'))


@app.route("/", methods=["GET"])
def root():
    return 'Syateki Center Server is running.'


if __name__ == "__main__":
    set_target()
    app.run("0.0.0.0")
