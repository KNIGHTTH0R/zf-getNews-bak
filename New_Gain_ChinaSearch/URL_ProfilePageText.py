# 通过URL获取页面信息——
# @zf - 2017.9.2
# coding=utf-8
import urllib
from http.cookiejar import CookieJar
from urllib.request import urlopen

import chardet
from bs4 import BeautifulSoup as BS


def DetailsPage(url):
    ProfileList = {}
    try:
        res2 = urllib.request.Request(url, None)  # f发送一个requet请求
        cj2 = CookieJar()  # 防反爬
        opener2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj2))
        response2 = opener2.open(res2)
        mychar2 = chardet.detect(
            response2.read())  # 获取编码字符串格式（如{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}）
        # print(mychar)
        bianma2 = mychar2['encoding']  # 获得网页编码（如utf-8）
        # print(bianma)
        res2 = urllib.request.Request(url, None)
        cj2 = CookieJar()
        opener2 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj2))
        response2 = opener2.open(res2)
        raw_response2 = response2.read().decode(bianma2, errors='ignore')
        response2.close()
        soup2 = BS(str(raw_response2), 'html.parser')
        # print(soup2)# 整个网页soup格式内容
        # p_text = soup2.find().text
        # p_text = str(p_text)
        # p_text = p_text.replace('  ', '')
        # print(p_text)
        # ProfileList = {}
        # print(ProfileList)
        Profile_HTML = str(soup2)
        # print(Profile_HTML)
    except Exception as e:
        print(str(e) + 'error——详细信息获取过程出错')
        Profile_HTML = 'error——详细信息获取过程出错'
        return Profile_HTML
    # print(p_text)
    return Profile_HTML


if __name__ == '__main__':
    url = 'http://www.chinanews.com/gj/2016/05-12/7867177.shtml'
    print('**********')
    DetailsPage(url)
    print('**********')
