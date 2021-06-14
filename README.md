# 一组简单的网页
2021/6/14

@xiangniLG 

## 介绍
豆瓣统计了基于他们自己算法的历史TOP250电影，但是他们做的网页里无关内容繁多，还有广告；所以为了更方便、直观地观察当前上映电影以及历史最优秀电影的情况，设计了一个小网站。

网站有三个页面：
1.  依据历史排名排序的历史前250电影的基本信息
2.  查询历史TOP250电影后返回的电影基本信息
3.  当前上映电影的票房等基础信息

目标人群：
1.  专业电影人
2.  电影院相关工作人员
3.  数据分析专业学生

## 系统需求
- python 3.7及以上
- MySQL 8.0及以上
- Navicat 数据库可视化软件（可选）

## 系统框架
    |--mywebsite
        |--README.md
        |--data_insert_database.py
        |--my_website.py
        |--static
            |--css
                |--realtime.css
                |--top250.css
            |--js
                |--echarts.min.js
                |--jquery.min.js
            |--douban
        |--templates
            |--moviedetails.html
            |--realtime1.html
            |--searchresult.html
模块分为两大部分，为建库和网站本体。

## 设计框架
### 终端
目前仅支持浏览器。推荐使用电脑浏览器，如chrome或firefox等。

网站总体流程图：

![终端流程图.png](https://i.loli.net/2021/06/14/eqkVLAbjfPQXRWd.png)

### 数据服务器
ER图：
![ER图.png](https://i.loli.net/2021/06/14/wUi7fXyMx8QCAHk.png)

数据字典：
| Field | Type | Collation | Null | Key | Default | Extra | Privileges | Comment |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- 
| movie_link     | varchar(255) | utf8_general_ci | YES  |     | NULL    |                | select,insert,update,references |         |
| movie_name     | varchar(255) | utf8_general_ci | YES  |     | NULL    |                | select,insert,update,references |         |
| movie_pic_link | varchar(255) | utf8_general_ci | YES  |     | NULL    |                | select,insert,update,references |         |
| movie_rating   | varchar(255) | utf8_general_ci | YES  |     | NULL    |                | select,insert,update,references |         |
| movie_director | varchar(255) | utf8_general_ci | YES  |     | NULL    |                | select,insert,update,references |         |
| movie_actor1   | varchar(255) | utf8_general_ci | YES  |     | NULL    |                | select,insert,update,references |         |
| movie_actor2   | varchar(255) | utf8_general_ci | YES  |     | NULL    |                | select,insert,update,references |         |
| movie_actor3   | varchar(255) | utf8_general_ci | YES  |     | NULL    |                | select,insert,update,references |         |
| id             | int          | NULL            | NO   | PRI | NULL    | auto_increment | select,insert,update,references |         |
| movie_pic_path | varchar(255) | utf8_general_ci | YES  |     | NULL    |                | select,insert,update,references |         |

### 网络安全
用的是华为的HECS服务器。安全组里，入方向规则开启了3个，分别为22、3389、5000，分别对应Linux默认的ssh端口、window远程控制端口和flask框架默认端口。

对于攻击，用了华为赠送的Agent服务，进行主机监控，包括基础监控，操作系统监控，进程监控。

## 启动网站
### 数据库搭建
对于数据库，请先按照数据字典建库/表。库名为moviedetails，表名为moviedetails.
### 数据入库
对于python 3.7以上版本，需提前安装如下包：
```
pip install fake-useragent
pip install beautifulsoup4
pip install Flask
pip install SQLAlchemy
pip install PyMySQL
```

在启动data_insert_database.py前，请在连接数据库的语句
```
db=pymysql.connect(
  user='',#用户名
  password='',#用户密码
  database='moviedetails',
  port=3306,
  charset='utf8'
)
```
修改为自己的用户名和密码，以进行数据库连接。

修改之后，启动data_insert_database.py。为了躲避豆瓣的反扒机制，进行了大量的休眠。

在爬虫结束后，请在static目录里的douban文件夹内检查图片文件数量是否为250.

在启动my_website.py前，请在连接数据库的语句
```
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://aaa:bbb@127.0.0.1:3306/moviedetails'
```
在aaa处填入自己数据库的用户名，bbb处填入对应的密码。

最后运行my_website.py,即可在本地端口5000进行网站的访问。

如果要将网站部署在服务器上，首先需要开放服务器的5000端口，然后修改my_website.py中的
```
app.run(port=5000)
```
改为
```
app.run(host='0.0.0.0',port=5000)
```
以进行服务主机的更换，再通过服务器的公网IP访问端口5000进行网站访问。

## 技术及技术难点
### 爬虫
爬虫使用了python的beautifulsoup4包，以方便进行对豆瓣网页内容的解析。bs4包可以通过lxml解析器解析网页，进而访问网页中的标签，并进行操作。

难点是，对抗豆瓣的反爬取机制。在项目前期经常在运行爬虫脚本时发现request得到的网页内容为空，发现已经被豆瓣墙掉了我的ip。

### 网页搭建
网页使用了Flask框架进行搭建。Flask连接数据库使用的是SQLAchemy，难点就在于这个库是用一种叫ORM(Object-Relational Mapping)的框架，把关系数据库的表结构映射到对象(类)上。所以之后对一个数据库的操作就变成了使用一个python类的方法。

这个库区别于PyMySQL的地方就在于这里。PyMySQL还是使用的是sql语句，再通过数据游标进行操作。

用户与数据库的交互是通过HTTPS的GET、POST方法实现的。在历史TOP250页面上有一个表单，用来搜索电影在历史上的排位，是通过request判断是否执行了POST方法后，将表单内容传递给SQLAchemy建立的对象，通过filter_by方法进行的检索，再返回搜索结果。

Flask建立网页是通过模板方法render_template进行参数传递。

## α测试
历史TOP250电影榜单：

![top.PNG](https://i.loli.net/2021/06/14/ROPZutoxWpw5hav.png)

电影搜索结果：

![searchresult.PNG](https://i.loli.net/2021/06/14/KWjDOiMF6t1z28G.png)

实时电影数据：

![realtime.PNG](https://i.loli.net/2021/06/14/nlANe4IYa8qcxWk.png)
  
