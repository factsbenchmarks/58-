import requests
from bs4 import BeautifulSoup
import time
import pymongo
client = pymongo.MongoClient('localhost',27017)
db = client['58city']
col = db['base_url']
base_url = 'http://bj.58.com/sale.shtml'
headers = {
        'Referer':'http://bj.58.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}

def get_type_base_url(url,times=0):
    '''
    爬取每类商品的主页，存储在mongodb中。
    :param url: 58同城首页
    :return: None
    '''

    if times == 3:
        return
    try:
        r = requests.get(url, headers=headers)
    except:
        return get_type_base_url(url,times+1)
    soup = BeautifulSoup(r.text, 'lxml')
    item_lists = soup.select('ul.ym-submnu > li > span > a')
    for item in item_lists:
        item_type_base_url = 'http://bj.58.com' + item.get('href')
        item_type_name = item.get_text()
        col.insert_one({'item_type_name': item_type_name,'item_type_base_url':item_type_base_url})  # 插入字典格式

get_type_base_url(base_url)

