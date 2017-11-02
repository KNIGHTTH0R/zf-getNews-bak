
# 传进百度搜索的新闻到mongoDB数据库，数据库名为：TestSinoMo，表名为：'_' + word_list + '_Baidu_News'
# # @zf - 2017.9.8
# __coding:utf-8__
# python version：3.5
# author:sharpdeep
import re
import urllib
import pandas as pd
import pymongo
import requests
from bs4 import BeautifulSoup as BS

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")


# from flask import Flask

# Search_N = Flask(__name__)
# @Search_N.route('/<company>/Search_News/',methods={"POST","GET"})
from News_Gain_BaiduSearch import URL_ProfilePageText
from News_Gain_BaiduSearch import Processing_profiles_One

def Search_News(word_list):
    try:
        n = 0
        try:
            word_list = word_list.replace('-', '').replace(' ', '')
            if "公司" in word_list:
                word_list = re.findall('(.+?)公司', word_list, re.S)
                word_list[0] = word_list[0] + "公司"
                word_list = str(word_list[0])
            else:
                word_list = word_list[0:15]
                # print(wordlist[0] + '            das')
        except Exception as e:
            print(str(e))
        # print(wordlist + '            123')
        # data_cdv = pd.DataFrame(
        #     columns=['id', 'Company_Name', 'New_URL', 'News_Soure', 'News_Time', 'News_Title', 'New_Details', 'News_HTML'])

        baseUrl = 'http://news.baidu.com/ns'
        for page in range(2):
            conn = pymongo.MongoClient('172.25.254.17:27017', 27017)
            # conn = pymongo.MongoClient('localhost:27017', 27017)
            # conn = pymongo.MongoClient(host='localhost', port=27017)
            db = conn['TestSinoMo']
            try:
                _table = db['_' + word_list + '_News']
            except Exception as e:
                print(str(e))
                continue

            data = {'word': word_list, 'pn=': str(page - 1) + '0', 'cl': '2', 'ct': '1', 'tn': 'news', 'rn': '20',
                    'ie': 'utf-8', 'bt': 0, 'et': 0}

            data = urllib.parse.urlencode(data)
            # print(data)
            url = baseUrl + '?' + data
            print(url)
            n = _table.find().count()
            try:
                html = requests.get(url)  # 获取网页
                html = html.text
                # html = urlopen(url)
                # print(html.read())
            except:
                continue
            # div = soup.find_all(class_='c-title')
            # div_str = html.find_all('div', class_='result')  # 查找属性是result"的div
            div_list = re.findall('<div class="result"(.+?)百度快照</a>', html, re.S)  # 获取百度中的一个新闻篇幅
            data_cdv = {}
            for list_1 in div_list:
                # break
                try:
                    list_URL = "<div class=\"result\"" + str(list_1) + "百度快照</a></span></div></div>"
                    list_URL = re.findall('http://[^\s]*?"', list_URL, re.S)
                    list_Soure_and_Time = re.findall('<p class="c-author">(.+?)</p>', list_1, re.S)
                    list_Soure_and_Time = str(list_Soure_and_Time[0])
                    list_Soure_and_Time = list_Soure_and_Time.split("&nbsp;")
                    # print(list_Soure_and_Time[2])
                    list_1 = list_1.replace(' ', '').replace('\n', '')
                    # print(list_1)
                    list_Title1 = re.findall('target="_blank">(.+?)</a>', list_1, re.S)
                    # print(list_Title1)
                    list_Title1 = str(list_Title1[0].replace('<em>', '').replace('</em>', ''))
                    # print(list_Title1)
                    # print(list_Title1[3:8])
                    results = _table.find_one(
                        {'News_Title': {'$regex': '^(.*?)' + list_Title1[3:8] + '(.*)'}})  # 用正则表达式判断title是否在mongoDB中
                    # print(results)
                    if results == None:
                        # for post in results:
                        # print("*****************************")
                        list_Details1 = re.findall('</p>(.+?)<spanclass="c-info"', list_1, re.S)
                        # print(list_1)
                        list_Details1 = str(list_Details1[0].replace('<em>', '').replace('</em>', ''))
                        # print(str(list_Details1))
                        list_URL = str(list_URL[0])
                        list_URL = list_URL.replace('[\'', '').replace('\"', '').replace('\']', '')
                        # print(list_URL)
                        News_HTML = URL_ProfilePageText.DetailsPage(list_URL)
                        soup = BS(News_HTML, 'html.parser')
                        list_Title2 = soup.find('title' or 'TITLE').text
                        # print(title)
                        # data_cdv["id"] = n
                        # data_cdv = {"id": n,
                        #             "Company_Name": word_list,
                        #             "New_URL": list_URL,
                        #             "News_Soure": list_Soure_and_Time[0],
                        #             "News_Time": list_Soure_and_Time[2],
                        #             "News_Title": list_Title1,
                        #             "News_HTML": News_HTML,
                        #             "New_Details": list_Details1
                        #             }
                        data_cdv["id"] = n
                        data_cdv["Company_Name"] = word_list
                        data_cdv["New_URL"] = list_URL
                        data_cdv["News_Soure"] = list_Soure_and_Time[0]
                        data_cdv["News_Time"] = list_Soure_and_Time[2]
                        data_cdv["News_Title"] = list_Title1
                        data_cdv["News_HTML"] = News_HTML
                        data_cdv["News_Details"] = list_Details1
                        data_cdv["Table_Souse"] = "百度搜索"
                        print(data_cdv)
                        _table.update_one({'id': data_cdv['id']}, {'$set': data_cdv}, True)
                        # print(word_list)
                        list_Details2 = Processing_profiles_One.processing_Pro_One(word_list + '_News', n)
                        # print(list_Details2)
                        _table.update_one({"id": n}, {'$set': {"News_Details": list_Details2}})
                        _table.update_one({"id": n}, {'$set': {"News_Title": list_Title2}})
                        n = n + 1
                    else:
                        continue
                except Exception as e:
                    list_Title2 = list_Title1
                    print(str(e))
                    continue
                    # print(data_cdv[0:3])
                    # dict = []
                    # dict.append()
                    # qwe = data_cdv.to_dict(orient="index")
                    # print(qwe)
                    # _table.update_many(qwe)
        return "true"
    except Exception as e:
        return "本次循环结束"


if __name__ == '__main__':
    # Search_N.run(host='localhost',port=8080)
    Search_News('芜湖造船厂')

