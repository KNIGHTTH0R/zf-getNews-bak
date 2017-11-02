# 通过官网获取公司简介地址——2017.9.2
# @zf - 2017.9.2
# coding=utf-8
import re
import urllib
from http.cookiejar import CookieJar
from urllib.request import urlopen
from eTensor_Spider_URL_details import URL_ProfilePageText
import chardet
from bs4 import BeautifulSoup as BS


def Detail_URL(url):
    # zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    Profile_navigation = ('集团简介', '企业概况', '集团介绍', '企业简介', '公司概况', '企业介绍', '公司介绍', '走进方圆', '关于我们')
    i = {1}
    detailslist = {}
    for a in i:
        try:
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
            # print(raw_response)
            # print(str(soup))
            # if "电话" in str(soup):
            for pro in Profile_navigation:
                # first_str = str(soup).replace('\n','')
                # print(soup)
                item = re.findall('<a href=(.*?)' + pro, str(soup), re.S)
                if item:
                    break
                else:
                    continue
            # print(item)
            item[0] = 'href=' + item[0]
            # print(item)
            if "href='" in str(item):
                # print(item[0] + '       1')
                item = re.findall(r"href=\'(.*?)\'", item[0])
                # print(str(item) + '3')
            else:
                # print(item[0] + '       2')
                item = re.findall(r"href=\"(.*?)\"", item[0])
                # print(str(item) + '3')
            # print(str(item))
            end_value = str(item[len(item) - 1])
            # print(end_value)
            end_value = end_value.replace('../', '').replace('./', '')
            s = re.match('/(.*?)', end_value)
            # print(end_value)
            if "http:" in end_value:
                url2 = end_value.replace('\'', '').replace('\"', '')
            else:
                url2 = end_value.replace('\"', '').replace('\'', '')
                url2 = url + url2
            url2 = url2.replace('&amp;', '&'.replace('&nbsp', ''))
            # if zh_pattern.search(url2):
            #     print('11111')
            # else:
            #     print('222222')
            # a = '企业介绍'
            # print(a.encode(mychar))
            print(url2)  # 输出公司详情的url
            # detailslist = URL_ProfilePageText.DetailsPage(url2)
            # print(detailslist)
            # else:
            #     try:
            #         print(url+'index_cn.php')
            #         Detail_URL(url+'index_cn.php')
            #         break
            #     except Exception as e:
            #         print(str(e) + 'error~~~获取URL错误')
            #         detailslist[0] = 'error'
            #         detailslist[1] = 'error'
            #         return detailslist
            #     break

        except Exception as e:
            print(str(e) + 'error~~~获取URL错误')
            return URL_ProfilePageText.DetailsPage('error~~~获取URL错误')
        # print(url2)
        return URL_ProfilePageText.DetailsPage(url2)


if __name__ == '__main__':
    url = 'http://www.csschps.com/'
    print('**********')
    Detail_URL(url)
    print('**********')
