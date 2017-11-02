# 通过官网循环获取公司title——2017.9.2
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
from New_Gain_ChinaSearch import Python_Juhe_ChinaSearch
from News_Gain_360Search import Python_Juhe_360Search
from News_Gain_BaiduSearch import Python_Juhe_BaiduSearch
from flask import Flask
app = Flask(__name__)

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
    for text_one in _table.find():
        title = text_one["title"]
        Baidu = Python_Juhe_BaiduSearch.Search_News(title)
        _360 = Python_Juhe_360Search.Search_News(title)
        China_New = Python_Juhe_ChinaSearch.Search_News(title)
        print("返回结果：" + Baidu + "..." + _360 + "..." + China_New) #+ _360 + "..." + China_New
if __name__ == '__main__':
    # Word_FS()
    app.run(host='localhost', port=8080)
    # for item in db.S1001.find():
    #     print(item)
