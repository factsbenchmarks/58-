import requests
from bs4 import BeautifulSoup
import pymongo
import hashlib
from multiprocessing import Pool
import os
from get_itembaseurl import get_type_base_url
from parse import get_detail_info,get_detail_url
client = pymongo.MongoClient('localhost',27017)
db = client['58city']
col = db['base_url']
base_urls = []
for item in col.find():
    base_urls.append(item['item_type_base_url'])


def get_all_detail_url(base_url):
    '''
    调用get_detail_url函数，爬取某种商品的的前N页所有商品的url。
    :param base_url:
    :return:
    '''
    for i in range(1,10):
        get_detail_url(base_url,i)

if __name__ == '__main__':
    p = Pool()
    p.map(get_all_detail_url,base_urls)
    p.close()
    p.join()
