--author:@张峰 

--time：@2017-9-7
#新闻爬虫
##1.基于搜索引擎(360搜索引擎)
###数据表名为：
>['_' + wordlist[0] + 'Baidu_News']

	描述：实例：“_江南造船厂_Baidu_News”
###关键词段为：
>['id', 'Company_Name', 'New_URL', 'News_Soure', 'News_Time', 'News_Title', 'New_Details']

	描述：此为存入mongoDB的字段

### 难点：

#####正则表达式 - 语法
>http://www.runoob.com/regexp/regexp-syntax.html

	描述:对搜到的文本进行匹配如:
		><div class="result" id="1">
			<h3 class="c-title">
				<a href="http://www.tlnews.cn/jsbb/2017-09/06/content_467416.htm"\n    data-click="{\n      \'f0\':\'77A717EA\',\n      \'f1\':\'9F63F1E4\',\n      \'f2\':\'4CA6DE6E\',\n      \'f3\':\'54E5343F\',\n      \'t\':\'1504757411\'}" target="_blank">
					拆迁六家<em>船厂</em> 保护长江岸线
				</a>
			</h3>
			<div class="c-summary c-row ">
				<p class="c-author">
					铜陵新闻网&nbsp;&nbsp;2017年09月06日 16:22
				</p>
					铜陵新闻网讯(崔彦沛 记者 方盼亮)为切实抓好环保督查问题整改工作,做好长江岸线资源保护、开发和利用,义安区老洲乡积极推进江边产生污染<em>船厂</em>搬迁工作。目前,该乡域...
				<span class="c-info">
					<a href="/ns?word=%E9%80%A0%E8%88%B9%E5%8E%82+cont:2073341276&same=3&cl=1&tn=news&rn=30&fm=sd" class="c-more_link" data-click="{\'fm\':\'sd\'}" >
						查看更多相关新闻>>
					</a>
					<a href="http://cache.baidu.com/c?m=9d78d513d9d437a94f9ae5697d10c015684381132ba7d1020cd1870fd33a541b0120a1ac26510d199680397001d80f02b6a77333200357e6c7d5d00b8deb8f282d8b2223706a844a0fd11db29a1b798777cc1cfea86de1bef53490aac5d3a80e1595&amp;p=906ecc15d9c240f903b1c7710f0e&amp;newp=aa6fc64ad4934eae59f3cf2a4a7a92695912c10e36ddc44324b9d71fd325001c1b69e3b823281603d4c6786c15e9241dbdb239256b55&user=baidu&fm=sc&query=%D4%EC%B4%AC%B3%A7&qid=914b82af0002cc36&p1=1"    data-click="{\'fm\':\'sc\'}" target="_blank" class="c-cache">
						百度快照
					</a>
				</span>
			</div>
		</div>
#####Python 字符串操作（string替换、删除、截取、复制、连接、比较、查找、包含、大小写转换、分割等）
>http://www.cnblogs.com/huangcong/archive/2011/08/29/2158268.html

	描述：对字符串的处理如对python二位数组的理解：
		>data_cdv = pd.DataFrame(
        columns=['id', 'Company_Name', 'New_URL', 'News_Soure', 'News_Time', 'News_Title', 'New_Details'])
    ID = 0
    Name = 0
    URL = 0
    Soure = 0
    Time = 0
    Title = 0
    Details = 0
    baseUrl = 'http://news.baidu.com/ns'


