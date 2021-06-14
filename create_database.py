import time
import pymysql
from fake_useragent import UserAgent
import requests
import os
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

download_path = './static/douban'
if not os.path.exists(download_path):
    os.makedirs(download_path)


def get_moviedetail(url):
  time.sleep(5)
  #time.sleep(20)
  ua = UserAgent()
  headers = {'User-Agent': ua.chrome}
  r = requests.get(url, headers = headers)
  soup = BeautifulSoup(r.text, 'lxml')
  content = soup.find('div', class_ = 'article')
  allspans=content.find('div',id='info')
  alldirector=allspans.find('a',rel="v:directedBy")
  director=alldirector.string
  allactors=allspans.find_all('a',rel="v:starring")
  actors=[]
  for actor in allactors:
    actors.append(actor.string)
  rating_div=content.find('strong',class_='ll rating_num')
  rating=rating_div.string
  return rating,director,actors

def get_data(url,mycursor,db):
  time.sleep(5)
  #time.sleep(20)
  ua = UserAgent()
  headers = {'User-Agent': ua.chrome}
  # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
  # 实现对网站的请求
  r = requests.get(url, headers = headers)
  # 使用BeautifulSoup进行解析
  soup = BeautifulSoup(r.text, 'lxml')    # 指定lxml解析器
  content = soup.find('div', class_ = 'article')   # 大的div
  if (content==None):
    input('no')
  images = content.find_all('img')   # 获取所有电影图片的标签
  hds=content.find_all('div',class_ ='hd')
  movie_detail_links=[]
  ratings=[]
  directors=[]
  actors=[]
  pic_address=[]
  for hd in hds:
    movie_detail_links.append(hd.a['href'])
  for movie_detail_link in movie_detail_links:
    [rating,director,actor]=get_moviedetail(movie_detail_link)
    ratings.append(rating)
    directors.append(director)
    if(actor==[]):
      actor1=["未知","未知","未知"]
      actor=actor1
    actors.append(actor)
  pic_link_list = [image['src'] for image in images]
  pic_name_list = [image['alt'] for image in images]
  for name in pic_name_list:
    pic_address.append('../static/douban/'+name+'.jpg')

  for detaillink , name, link,rating,director,actor,address in zip(movie_detail_links, pic_name_list, pic_link_list,ratings,directors,actors,pic_address):
    urlretrieve(link, f'{download_path}/{name}.jpg')
    sql="insert into moviedetails(movie_link,movie_name,movie_pic_link,movie_rating,movie_director,movie_actor1,movie_actor2,movie_actor3,pic_address)\
         values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    values=(detaillink , name, link,rating,director,actor[0],actor[1],actor[2],address)
    mycursor.execute(sql,values)
    db.commit()
  print(f'{url}爬虫完成')


db=pymysql.connect(
  user='root',
  password='xiangniLG',
  database='moviedetails',
  port=3306,
  charset='utf8'
)
mycursor=db.cursor()
start_urls = ['https://movie.douban.com/top250']

for i in range(1, 10):
  start_urls.append(f'https://movie.douban.com/top250?start={25 * i}&filter=')

get_data(start_urls[0],mycursor,db)
# for url in start_urls:
#   get_data(url,mycursor,db)

mycursor.close()
db.close()







