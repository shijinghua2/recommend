import os
import uuid
import datetime
import redis
import sqlite3
import json


class Dao:   
    # pool = redis.ConnectionPool(host='47.106.32.55', port=6379, decode_responses=True)
    def __init__(self):
        self.redis=redis.Redis(host='47.106.32.55',port=6379, db=0,password='sjhdabendan')    
        try:        
            p = os.path.dirname(__file__)
            self.sqlite = sqlite3.connect(os.path.join(p, '../Data/Book.db'), check_same_thread=False)
        except Exception as e:
            print(e)
        self.sqlcursor =self.sqlite.cursor()

    # 获取评分最高的书
    def get_top_books(self,num=10):
        key = 'topbooks_100'
        cacheds = self.redis.get(key)
        if cacheds == None or cacheds == '':
            # 从数据库里取出
            self.sqlcursor.execute('select * from [BX-Books] order by [Book-Avg-Rating] desc limit 0,100')
            dbed=self.sqlcursor.fetchall()
            datas=[]
            for row in dbed:
                datas.append({
                    'isbn': row[0],
                    'title': row[1],
                    'author': row[2],
                    'year': row[3],
                    'publisher': row[4],
                    'imgs': row[5],
                    'imgm': row[6],
                    'imgl': row[7],
                    'avgr': row[8]
                })
        
            # 存到redis中
            self.redis.set(key,json.dumps(datas),60*60)
        else:
            datas = json.loads(cacheds)
        num = 20 if num>20 else (num if num>0 else 10)
        return JSON.dumps(datas[:num])
        
    # 获取评分最高的标签
    def get_top_tags(self, num=10):
        if tagid is None:
            return []
        key = 'toptags_100'
        cacheds = self.redis.get(key)
        if cacheds == None or cacheds == '':
            # 从数据库里取出
            self.sqlcursor.execute('select * from [BX-Tags] order by [Rate-Avg] desc limit 0,100')
            dbed = self.sqlcursor.fetchall()
            datas = []
            for row in dbed:
                datas.append({
                    'id': row[0],
                    'name': row[1],
                    'avgr': row[2]
                })

            # 存到redis中 缓存1小时
            self.redis.set(key, json.dumps(datas), 60*60)
        else:
            datas = json.loads(cacheds)
        num = 20 if num > 20 else (num if num > 0 else 10)
        return json.dumps(datas[:num])

    # 获取某一标签评分最高的书
    def get_top_tag_books(self,tagid, num=10):
        key = 'topbooks_100'
        cacheds = self.redis.get(key)
        if cacheds == None or cacheds == '':
            # 从数据库里取出
            self.sqlcursor.execute(
                'sselect * from [bx-books] where isbn in (select isbn from [bx-book-tags] where [tag-id]={0}) order by [book-avg-rating] desc limit 0,100'.format(tagid))
            dbed = self.sqlcursor.fetchall()
            datas = []
            for row in dbed:
                datas.append({
                    'isbn': row[0],
                    'title': row[1],
                    'author': row[2],
                    'year': row[3],
                    'publisher': row[4],
                    'imgs': row[5],
                    'imgm': row[6],
                    'imgl': row[7],
                    'avgr': row[8]
                })

            # 存到redis中
            self.redis.set(key, json.dumps(datas), 60*60)
        else:
            datas = json.loads(cacheds)
        num = 20 if num > 20 else (num if num > 0 else 10)
        return json.dumps(datas[:num])
    
    # 登陆
    def login(self, uid):
        # 从数据库里取出
        self.sqlcursor.execute('select * from [bx-Users] where [User-ID]='+str(uid))
        dbed = self.sqlcursor.fetchone()
        if dbed is None:
            return -1
        user={
            'uid':dbed[0],
            'location':dbed[1],
            'age':dbed[2]
        }
        guid = str(uuid.uuid1())
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.sqlcursor.execute('delete from [bx-login] where [user-id]='+str(uid))
        self.sqlcursor.execute("insert into [bx-login] values({0},'{1}','{2}')".format(uid, guid, now))
        self.sqlite.commit()
        user['guid']=guid
        return json.dumps(user)

    # 退出登录
    def logout(self, guid):
        # 从数据库里取出
        self.sqlcursor.execute(
            'delete from [bx-login] where [user-id]='+str(uid))
        self.sqlite.commit()
        return 1

    def __del__(self):
        self.sqlite.close()

if __name__=='__main__':
    dao = Dao()
    print(dao.login(13))
