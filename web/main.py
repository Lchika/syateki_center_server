from flask import Flask, request
import urllib.request
import ssl
import re

app = Flask(__name__)

def get_target_num(response):
    return re.search(r'(?<==)\d+', response).group()

@app.route("/", methods=["GET"])
def get_shoot():
    if request.method == "GET":
        ssl._create_default_https_context = ssl._create_unverified_context
        url_target = 'http://192.168.100.125'
        headers = {}
        req = urllib.request.Request(url_target)
        target_num = '0'
        with urllib.request.urlopen(req) as res:
            res_html = res.read().decode('utf-8')
            print('score_site res = ' + res_html)
            target_num = get_target_num(res_html)
            print('target_num = ' + target_num)
        return target_num

if __name__ == "__main__":
    app.run("0.0.0.0")

