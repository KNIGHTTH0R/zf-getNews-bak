# 通过百度获取公司官网地址——2017.9.2
# @zf - 2017.9.2
# coding=utf-8
# coding=utf-8
# python version：3.5
# author:sharpdeep
import re
import urllib
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup as BS


def sousuo(word, bs=None):
    data_csv = pd.DataFrame(columns=['title', 'link', 'time', 'desc'])
    x = 0
    y = 0
    z = 0
    k = 0
    baseUrl = 'http://www.baidu.com/s'
    links = []
    for page in range(1, 20):
        data = {'wd': word, 'pn': str(page - 1) + '0', 'tn': 'baidurt', 'ie': 'utf-8', 'bsst': '1',
                'bs': 'filetype:xls 机械'}
        data = urllib.parse.urlencode(data)
        # print(data)
        url = baseUrl + '?' + data
        # print (url)

        try:
            html = urlopen(url)
        # except urllib2.HttpError,e:
        #     print e.code
        #     exit(0)
        # except urllib2.URLError,e:
        #     print e.reason
        #     exit(0)
        except:
            continue

        # html = response.read()
        soup = BS(html, 'html.parser')
        # print(soup)
        td = soup.find_all(class_='f')
        # print(td)
        for t in td:
            a = t.h3.a.get_text()  # 搜索出来的title
            a1 = re.sub('\s+', '', a)
            # print(a1)
            data_csv.loc[x, 'title'] = a1
            x = x + 1
            b = t.h3.a['href']
            b1 = re.sub('\s+', '', b)
            # print(b1)
            data_csv.loc[y, 'link'] = b1
            y = y + 1
            font_str = t.find_all('font', attrs={'size': '-1'})[0].get_text()
            # print(font_str)
            start = 0  # 起始
            realtime = t.find_all('div', attrs={'class': 'realtime'})
            if realtime:
                realtime_str = realtime[0].get_text()
                start = len(realtime_str)
                c = realtime_str
                data_csv.loc[z, 'time'] = c
                z = z + 1
            end = font_str.find('...')
            d = font_str[start:end + 3]
            # print(d)
            data_csv.loc[k, 'desc'] = d
            k = k + 1
            links.append(b1)
    return links
    # print(links)
    # print (data_csv)
    # for n in data_csv.index:
    #     a=data_csv.loc[n,'time']
    #     if(re.search(u'天前',a)):
    #         data_csv.loc[n,'daynum']=float(re.sub(u'天前','',a))
    #     elif(re.search(u'小时前',a)):
    #         data_csv.loc[n,'daynum']=float(re.sub(u'小时前','',a))/24
    #     else:
    #         continue

    # print (data_csv.sort_index(by='daynum'))


if __name__ == '__main__':
    word = input('输入关键字：')
    # print('在右边的查询格式中选择想要的格式输入：filetype:xls加空格 ，filetype:pdf加空格 ，filetype:ppt加空格，filetype:doc加空格 ，filetype:rtf加空格')
    # bs = input('我的格式是： (可不填)')
    # type=input('选择查询格式')
    result = sousuo(word, bs=None)
    print(result)
