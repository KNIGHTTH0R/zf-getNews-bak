# 通过官网循环获取公司title——2017.9.2
# @zf - 2017.9.2
# coding=utf-8

import re
import urllib
from http.cookiejar import CookieJar
from eTensor_Spider_URL_details import Detail_url
from eTensor_Spider_URL_details import Processing_profiles_One
from eTensor_Spider_URL_details import baidu_python3
import chardet
import pymongo
from bs4 import BeautifulSoup as BS
from flask import Flask

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


@app.route('/<word>/input_search', methods={"POST", "GET"})
def Word_FS(word):
    # word = input('输入关键字：')
    # print('在右边的查询格式中选择想要的格式输入：filetype:xls加空格 ，filetype:pdf加空格 ，filetype:ppt加空格，filetype:doc加空格 ，filetype:rtf加空格')
    # bs = input('我的格式是： (可不填)')
    conn = pymongo.MongoClient('172.25.254.17:27017', 27017)
    # db = conn.TestSinoMo
    # conn = pymongo.MongoClient('localhost:27017', 27017)
    # collection = db.word（链接建立数据库方法1）
    db = conn['TestSinoMo']
    _table = db['_' + word]
    # type=input('选择查询格式')
    links = baidu_python3.sousuo(word, bs=None)

    # print(links)
    i = 0
    data = {}
    for url in links:
        # print(link)
        if (re.match('.*?.com/$', url)) or (re.match('.*?.com.cn/$', url)) or (re.match('.*?.cn/$', url)):
            detailslist = {}
            try:
                # print(url)
                res = urllib.request.Request(url, None)  # f发送一个requet请求
                cj = CookieJar()  # 防反爬
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
                response = opener.open(res)
                mychar = chardet.detect(
                    response.read())  # 获取编码字符串格式（如{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}）
                # print(mychar)
                bianma = mychar['encoding']  # 获得网页编码（如utf-8）
                # print(bianma)
                res = urllib.request.Request(url, None)
                cj = CookieJar()
                opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
                response = opener.open(res)
                raw_response = response.read().decode(bianma, errors='ignore')
                response.close()
                soup = BS(raw_response, 'html.parser')
                title = soup.find('title' or 'TITLE').text
                title = re.sub('\n', '', title)
                title = re.sub('网站首页', '', title)
                title = re.sub('首页', '', title)
                title = re.sub('\t', '', title)
                title = title.lstrip()
                print(title)  # 输出公司title
            except Exception as e:
                print(str(e))
                continue
            print(url)  # 输出公司官网
            # print(raw_response)# 输出整个网页
            Profile_HTML = Detail_url.Detail_URL(url)
            # print(detailslist)
            # Details_List = _table.find_one({"id":i})
            # if "false" in str(Details_List["details"]):
            data["id"] = i
            data["url"] = url
            data["title"] = title
            data["details"] = "[处理失败！]"
            data["detailsPageText"] = Profile_HTML

            data["indexPage"] = raw_response
            _table.update_many({'id': data['id']}, {'$set': data}, True)
            deal_Details2 = Processing_profiles_One.processing_Pro_One(word, i)
            _table.update({"id": i}, {'$set': {"details": deal_Details2}})
            if "false" in deal_Details2:
                print("详情处理失败，没有存入！")
            elif "error" in Profile_HTML:
                print("详情处理失败，没有存入！")
            else:
                print("详情处理成功！！")
            # elif "[]" in str(Details_List["details"]):
            #     data["id"] = i
            #     data["url"] = url
            #     data["title"] = title
            #     data["details"] = "[处理失败！]"
            #     data["detailsPageText"] = Profile_HTML
            #     data["indexPage"] = raw_response
            #     _table.update_many({'id': data['id']}, {'$set': data}, True)
            #     deal_Details2 = Processing_profiles_One.processing_Pro_One(word, i)
            #     _table.update({"id": i}, {'$set': {"details": deal_Details2}})
            #     if "false" in deal_Details2:
            #         print("详情处理失败，没有存入！")
            #     elif "error" in Profile_HTML:
            #         print("详情处理失败，没有存入！")
            #     else:
            #         print("详情处理成功！！")
            i = i + 1

            # Processing_profiles('' + word)


if __name__ == '__main__':
    # Word_FS()
    app.run(host='localhost', port=8080)
    # for item in db.S1001.find():
    #     print(item)
