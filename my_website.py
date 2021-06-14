from flask import Flask, request, flash, url_for, redirect, render_template,session
from fake_useragent import UserAgent
import requests
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://aaa:bbb@127.0.0.1:3306/moviedetails'#aaa为用户名，bbb为密码。请修改为自己的数据库用户名与密码
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = "False"

db = SQLAlchemy(app)

def get_data():
  url="https://piaofang.maoyan.com/getBoxList?date=1&isSplit=true"
  myheaders={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
  mydata=requests.get(url,headers=myheaders).text
  mydata1=json.loads(mydata)
  return mydata1


class moviedetails(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   movie_link = db.Column(db.String(100))
   movie_name = db.Column(db.String(50))
   movie_pic_link = db.Column(db.String(200)) 
   movie_rating = db.Column(db.String(200)) 
   movie_director = db.Column(db.String(200)) 
   movie_actor1 = db.Column(db.String(200)) 
   movie_actor2 = db.Column(db.String(200)) 
   movie_actor3 = db.Column(db.String(200))
   movie_pic_path = db.Column(db.String(200))

   def __init__(self, id, movie_link, movie_name, movie_pic_link, movie_rating, movie_director, movie_actor1, movie_actor2, movie_actor3,movie_pic_path):
      self.id = id
      self.movie_link = movie_link
      self.movie_name = movie_name
      self.movie_pic_link = movie_pic_link
      self.movie_rating = movie_rating
      self.movie_director = movie_director
      self.movie_actor1 = movie_actor1
      self.movie_actor2 = movie_actor2
      self.movie_actor3 = movie_actor3
      self.movie_pic_path = movie_pic_path



@app.route('/top',methods=['POST','GET'])
def top(): 
  return render_template('moviedetails.html', moviedetails = moviedetails.query.all())

@app.route('/realtimeInfo')
def realtimeInfo():
  # while(True):
  #   time.sleep(10)
  realtimemovieInfo=get_data()
  real={'boxdescList':[],'boxrateList':[],'movienameList':[],'sumBoxDesc':[],'fullmovienameList':[],'fullboxrateList':[]}
  for i in range(0,15):
    real['boxdescList'].append(float(realtimemovieInfo["boxOffice"]['data']['list'][i]['boxDesc']))
    real['boxrateList'].append(float(realtimemovieInfo["boxOffice"]['data']['list'][i]['boxRate'][0:-1])/100)
    real['fullboxrateList'].append(float(realtimemovieInfo["boxOffice"]['data']['list'][i]['boxRate'][0:-1])/100)
    real['movienameList'].append(realtimemovieInfo["boxOffice"]['data']['list'][i]['movieInfo']['movieName'])
    real['fullmovienameList'].append(realtimemovieInfo["boxOffice"]['data']['list'][i]['movieInfo']['movieName'])
    c=float(realtimemovieInfo["boxOffice"]['data']['list'][i]['sumBoxDesc'][0:-1])
    danwei=realtimemovieInfo["boxOffice"]['data']['list'][i]['sumBoxDesc'][-1]
    if danwei=='亿':
      c=round(c*10000)
      real['sumBoxDesc'].append(c)
    else:
      c=round(c)
      real['sumBoxDesc'].append(c)
  real['fullmovienameList'].append('其他')
  real['fullboxrateList'].append(round((1-sum(real['boxrateList']))*100)/100)
  return render_template('realtime1.html',realtimemovieInfo=real)

@app.route('/searchresult',methods=['POST','GET'])
def searchresult():
  if request.method == 'POST':
    moviename = request.form.get('moviename')
    return render_template('searchresult.html',moviedetails = moviedetails.query.filter_by(movie_name=moviename).all())


if __name__ == '__main__':
   db.create_all()
   app.run(port=5000)
