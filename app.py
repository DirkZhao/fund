# encoding: utf-8
import requests
import json
import re

from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZHAO'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/ping', methods=['POST', 'GET'])
def ping():
    result = 'ping OK!'
    if request.method == 'POST':
        print(request.form)
    else:
        print(request.args)
        result = result + str(request.args)
    return result


@app.route('/fund/<fund_code>', methods=['POST', 'GET'])
def fund_info(fund_code):
    # 汇添富创新医药主题混合：006113
    # 易方达消费行业股票：110022
    # 嘉实新兴产业股票：000751
    # 交银海外中国互联网指数：164906
    url = "http://fundgz.1234567.com.cn/js/{0}.js".format(fund_code)
    # 浏览器头
    headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    r = requests.get(url, headers=headers)
    # 返回信息
    content = r.text

    # 正则表达式
    pattern = r'^jsonpgz\((.*)\)'
    # 查找结果
    search = re.findall(pattern, content)
    # 遍历结果
    data = ""
    for i in search:
        data = json.loads(i)

    fund_name = data['name']
    fund_prize = data['dwjz']
    fund_date = data['jzrq']
    '''print("基金名称：{0} \n"
          "基金代码：{1} \n"
          "日期：{2} \n"
          "净值：{3}".format(fund_name, fund_code, fund_date, fund_prize))'''

    return "基金名称：{0} \n 基金代码：{1} \n 日期：{2} \n 净值：{3}".format(fund_name, fund_code, fund_date, fund_prize)


if __name__ == '__main__':
    app.run()
