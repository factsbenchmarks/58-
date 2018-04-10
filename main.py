import requests
from bs4 import BeautifulSoup
import pymongo
import hashlib
from multiprocessing import Pool
import os
from get_itembaseurl import get_type_base_url,col
from parse import get_detail_info,get_detail_url,col_detail_url

base_urls = [ item['item_type_base_url']for item in col.find()]
detail_urls = [ item['detail_url']for item in col_detail_url.find()]
print(detail_urls)
def get_all_detail_url(base_url):
    '''
    调用get_detail_url函数，爬取某种商品的的前N页所有商品的url。
    :param base_url:
    :return:
    '''
    for i in range(1,2):
        get_detail_url(base_url,i)

if __name__ == '__main__':
    p = Pool()
    #多线程爬取所有商品的url,保存到mongodb中
    # p.map(get_all_detail_url,base_urls)
    # p.close()
    # p.join()
    #多线程爬取商品的详细信息，保存到mongodb中
    p.map(get_detail_info,detail_urls)
    p.close()
    p.join()
