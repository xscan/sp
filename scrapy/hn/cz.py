import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time 

projectName="郴州市公共资源交易中心"

class Item(object):
    def __init__(self,title,url,date) -> None:
        self.title = title
        self.url = url
        self.date = date
        pass

    def toString(self):
        return "{2} {0}:{1} ".format(self.title,self.url,self.date)

def get_random_ua(): #随机UA
    ua = UserAgent()
    return ua.random

def getBaseUrl(baseUrl):
    index = baseUrl.rfind("/")
    s = baseUrl[0:index+1]
    return s
    pass

def scrapy(baseUrl):
    headers = {
        'User-Agent': get_random_ua()
    }
    res = requests.get(url=baseUrl, headers=headers,timeout=10)
    res.encoding = 'gb2312'
    selector = BeautifulSoup(res.text,"lxml")

    bodylist = selector.select(".list-ul li")
    list_items = []
    baseHost = getBaseUrl(baseUrl)
    for item in bodylist:
        title = item.select('a')[0].attrs['title']
        url =  baseHost+item.select('a')[0].attrs['href']
        date = item.select('span')[0].text
        list_items.append(Item(title,url,date))

    return list_items

types = [
    {
        "baseUrl":"http://czggzy.czs.gov.cn/18360/18370/18371/18382/18383/index.htm",
        "type":"房屋市政"
    },
    {
        "baseUrl":"http://czggzy.czs.gov.cn/18360/18370/18371/18382/18384/index.htm",
        "type":"交通"
    },
    {
        "baseUrl":"http://czggzy.czs.gov.cn/18360/18370/18371/18382/18385/index.htm",
        "type":"水利"
    },
    {
        "baseUrl":"http://czggzy.czs.gov.cn/18360/18370/18371/18382/18386/index.htm",
        "type":"其他"
    },
    {
        "baseUrl":"http://czggzy.czs.gov.cn/18360/18370/18371/18382/18387/index.htm",
        "type":"代理公告"
    },
]

listItem = []
for type in types:
   
    typeList = scrapy(type['baseUrl'])
    for item in typeList:
        item.type=type['type']
        listItem.append(item)
    
    print(time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime()),"爬取",projectName,type['type'],str(len(typeList))+"条")

# 写入文件
# 增量更新问题

print(listItem) 
print([i.toString() for i in listItem])


