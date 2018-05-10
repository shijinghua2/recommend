import os
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

    def get_top_books(self,num):
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
            
            print(json.dumps(datas))
            # 存到redis中
            self.redis.set(key,json.dumps(datas),60*60)
        else:
            datas = json.loads(cacheds)
            print(datas)
        
            


    def __del__(self):
        self.sqlite.close()

if __name__=='__main__':
    dao = Dao()
    dao.get_top_books(10)
