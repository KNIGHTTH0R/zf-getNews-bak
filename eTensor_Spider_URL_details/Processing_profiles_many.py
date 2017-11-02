# 传进参数为表名，对表中所有的html进行处理，提取页面中的有用文章
# @zf - 2017.9.2
import re

import pymongo


def processing_Pro(word):
    try:
        conn = pymongo.MongoClient('172.25.254.17:27017', 27017)
        # collection = db.word（链接建立数据库方法1）
        db = conn['TestSinoMo']
        _table = db['_' + word]
        for Details_List in _table.find():
            # print(Details_List)
            id = Details_List["id"]
            title = Details_List["title"]
            details_zz = Details_List["detailsPageText"]
            deal_Details = re.sub('\n\n', '', details_zz)
            Details_List = deal_Details.split("\n")
            deal_Details2 = []
            for list_1 in Details_List:  # 循环判断是否有中文符号并保留
                if "，" in str(list_1):
                    deal_Details2.append(list_1)
                elif "。" in list_1:
                    deal_Details2.append(list_1)
            deal_Details2 = str(deal_Details2)  # 数组转化为字符串
            dr = re.compile(r'</?\w+[^>]*>', re.S)
            deal_Details2 = re.sub(dr, '', deal_Details2)
            deal_Details2 = re.sub('<[^>]+>', '', deal_Details2)
            deal_Details2 = deal_Details2.replace('\\xa0', '').replace('[\'', '')
            deal_Details2 = deal_Details2.replace('\\t', '').replace('\']', '').replace('\\r', '')
            deal_Details2 = deal_Details2.replace('\\u3000', '').replace(" ", '').replace('\',\'', '')
            _table.update({"id": id}, {'$set': {"details": deal_Details2}})
            print(str(id) + ":    " + deal_Details2)
    except:
        return "false"
    return "true"


if __name__ == '__main__':
    url = 'http://www.wh-shipyard.com/'
    processing_Pro('造船厂')
