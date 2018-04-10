import requests
from bs4 import BeautifulSoup
import pymongo
import hashlib
import time
flag = '很抱歉，没有找到相关信息'
client = pymongo.MongoClient('localhost',27017)
db = client['58city']
col = db['base_url']
col_detail_url = db['detail_url']
col_detail_info = db['detail_info']

headers = {
        'Referer':'http://bj.58.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}

def get_detail_url(base_url,page,times=0):
    '''
    传入base_url,传入某个页码，返回当前这个页码的所有的detail的url，并保存到mongodb中。
    :param base_url:
    :param page:
    :return:
    '''
    if times == 3:
        return
    url = base_url + 'pn{}'.format(page)
    try:
        r = requests.get(url)
    except:
        return get_detail_url(url,page,times+1)  #加了异常处理，本质是递归函数
    if flag in r.text:   # 某类商品的某页，可能不存在。判断，58同城服务器有没有这个页面。
        pass
    else:
        soup = BeautifulSoup(r.text,'lxml')
        detail_as = soup.select('td.t > a')
        for item in detail_as:
            detail_url = item.get('href')
            if detail_url.startswith('http://zhuanzhuan.58.com'):  # 排除干扰项
                col_detail_url.insert_one({'detail_url':detail_url})
def get_detail_info(url,times=0):
    '''
    爬取某个商品的想象信息，并保存到mongodb中，
    :param url:
    :return:
    '''
    time.sleep(1)
    if times == 3:
        return
    try:
        r = requests.get(url, headers=headers)
    except:
        return get_detail_info(url,times+1)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find('h1', class_='info_titile').get_text() if soup.find('h1', class_='info_titile') else None
    price = soup.select('span.price_now > i')[0].get_text() if soup.select('span.price_now > i') else None
    zone = soup.select('div.palce_li > span > i')[0].get_text() if soup.select('div.palce_li > span > i') else None
    desc = soup.select('div.baby_kuang > p')[0].get_text() if soup.select('div.baby_kuang > p') else None
    detailurl = url
    if title or price or zone or desc:
        col_detail_info.insert_one({'title': title, 'price': price, 'zone': zone, 'desc': desc, 'detailurl': detailurl})

# def md5(url):
#     m = hashlib.md5()
#     m.update(bytes(url,encoding='utf-8'))
#     return m.hexdigest()
# def record(db,url):
#     col = db['record']
#     key = md5(url)
#     col.insert_one({key:True})
#
# def check(db,url):
#     col = db['record']
#     res = md5(url)
#     if  col.find_one({res:True}):
#         return False
#     else:
#         return True
