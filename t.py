import requests
from bs4 import BeautifulSoup
import pymongo
client = pymongo.MongoClient('localhost',27017)
db58 = client['58']
house58 = db58['house58']

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Referer':'http://bj.58.com/',
}



def save_item(url):
    res = requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text,'lxml')
    price = soup.find('b',class_='f36').get_text() if soup.find('b',class_='f36') else None

    phone = soup.find('span',class_='house-chat-txt').get_text() if soup.find('span',class_='house-chat-txt') else None
    if price and phone:
        house58.insert_one({
            'price':int(price),
            'phone':phone
        })
urls = ['http://bj.58.com/chuzu/pn{}/'.format(i) for i in range(1,4)]

for url in urls:
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    items = soup.select('div .img_list a')
    for item in items:
        if item.get('href'):
            save_item(item['href'])

