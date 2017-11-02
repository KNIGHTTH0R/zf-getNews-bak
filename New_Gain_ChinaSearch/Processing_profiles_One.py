# 传进参数为表名，对表中对应id的html进行处理，提取页面中的有用文章
# @zf - 2017.9.8
import re
import pymongo
def processing_Pro_One(word, ids):
    try:
        # print(word)
        conn = pymongo.MongoClient('172.25.254.17:27017', 27017)
        # collection = db.word（链接建立数据库方法1）
        # conn = pymongo.MongoClient('localhost:27017', 27017)
        db = conn['TestSinoMo']
        _table = db['_' + word]
        # print(Details_List)
        Details_List = _table.find_one({"id": ids})
        # print(Details_List)
        # title = Details_List["title"]
        details_zz = Details_List["News_HTML"]  # 取出没有处理的html
        # print(details_zz)
        deal_Details = re.sub('\n\n', '', details_zz)
        Details_List = deal_Details.split("\n")
        deal_Details2 = []
        for list_1 in Details_List:  # 循环判断是否有中文符号并保留
            # if "，" in str(list_1):
            #     deal_Details2.append(list_1)
                # print(list_1)
            if "。" in list_1:
                deal_Details2.append(list_1)
                # print(list_1)
        # print(len(deal_Details2)-1)
        deal_Details2 = str(deal_Details2)  # 数组转化为字符串
        dr = re.compile(r'</?\w+[^>]*>', re.S)
        deal_Details2 = re.sub(dr, '', deal_Details2)
        deal_Details2 = re.sub('<[^>]+>', '', deal_Details2)
        deal_Details2 = deal_Details2.replace('\\xa0', '').replace('[\'', '')
        deal_Details2 = deal_Details2.replace('\\t', '').replace('\']', '').replace('\\r', '')
        deal_Details2 = deal_Details2.replace('\\u3000', '').replace(" ", '').replace('\',\'', '')

        deal_Details2 = re.findall("summary:(.+?)summary:", deal_Details2, re.S)  # 2017-9-12 #zf改  取中国询问网中summary:中间的字符串
        deal_Details2 = str(deal_Details2[0])
        # print(str(ids) + "   :" + deal_Details2)

    except:
        return "false"
    return deal_Details2


if __name__ == '__main__':
    url = 'http://www.chinanews.com/gj/2016/05-12/7867177.shtml'
    print("*****************************************")
    processing_Pro_One('中航威海船厂有限公司_News', 0)
    print("*****************************************")
