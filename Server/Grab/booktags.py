import os
import csv
import sqlite3
import threading
import time
from googlebookapi import Api

import sys
sys.setrecursionlimit(1000000)
p=os.path.dirname(__file__)
conn = sqlite3.connect(os.path.join(p,'../Data/Book.db'), check_same_thread=False)
c=conn.cursor()
# 获取书本的个数，方便后面遍历寻找
c.execute('select max(rowid) from [bx-books]')
x=c.fetchone()
conn.close()
maxRowId=x[0]
sem = threading.RLock()
alltags = ['']
failISBN = []
# a=c.execute('insert into [bx-tags](name) values(\'a\')')
# tag='b'
# c.execute('select id from [bx-tags] where name=\'{0}\''.format(tag))
# print(c.fetchone())
curindex=0
def genBash(begin,step,max):
    conn = sqlite3.connect(os.path.join(p, '../Data/Book.db'), check_same_thread=False)
    c = conn.cursor()
    invalid=False
    end=begin+step
    print(':::::::::::::::::::begin:{0},end:{1}:::::::::::::::::::::'.format(begin,end))
    sem.acquire()
    # 筛选出这一批需要查找的书本
    c.execute('select [ISBN],[Book-Avg-Rating] from [BX-Books] where isbn not in (select isbn from [bx-book-tags]) and isbn not in (select isbn from [bx-invalidbooks]) and rowId>{0} and rowId<={1}'.format(begin, end))
    cc=c.fetchall()
    sem.release()
    for row in cc:
        isbn=row[0]
        print(isbn+"==> begin...")
        score = int(row[1])        
        try:
            api = Api()
            # 使用Google Book Api 根据ISBN获取图书信息
            book = api.list('isbn:{0}'.format(isbn))
        except Exception as error:
            print('\t{0} get book error => {1}',isbn,error)
            book=None
            failISBN.append(isbn)
        if book is None:
            continue
        if 'totalItems' not in book or book['totalItems']==0:
            if hasattr(book,'status_code') and book.status_code==403:
                print('google api invalid')
                invalid = True
                break
            else:
                sem.acquire()
                c.execute('insert into [bx-invalidbooks](isbn) values(\'{0}\')'.format(isbn))
                conn.commit()
                sem.release()
                print('\t{0} totalItems not in book'.format(isbn))
                print('\t{0}'.format(book))
                continue
        try:
            # 获取图书类别
            tags=book['items'][0]['volumeInfo']['categories']
        except KeyError:
            print('\t{0} keyerror no categories in book '.format(isbn))
            sem.acquire()
            c.execute('insert into [bx-invalidbooks](isbn) values(\'{0}\')'.format(isbn))
            conn.commit()
            sem.release()
            tags=None
        except Exception as error:
            print('\t{0} error:{1}'.format(isbn,error))
            tags=None
        if tags is None or len(tags)==0:
            continue
        print('\t{0} tags:{1}'.format(isbn,str(tags)))
        
        # 本书的所有标签
        for tag in tags:
            try:
                sem.acquire()
                # 获取标签
                c.execute('select id from [bx-tags] where name=\'{0}\''.format(tag.replace("'", "''")))
                fone=c.fetchone()
                if fone is None:
                    temp=c.execute('insert into [BX-Tags](name) values(\'{0}\')'.format(tag.replace("'","''")))
                    tagid = temp.lastrowid
                    print('\t{0}=>insert,id is => {1}'.format(tag,tagid))
                else:
                    tagid=fone[0]
                    print('\t{0}=>select,id is => {1}'.format(tag, tagid))
                # 将书和标签的映射关系放在
                c.execute('insert into [BX-Book-Tags](ISBN,[Tag-ID],[Rate]) values(\'{0}\',{1},{2})'.format(isbn, tagid, score))
                conn.commit()
                sem.release()
            except Exception as error:
                print('\t{0} execute sql error :{1}'.format(isbn,error))
                continue


    
    

    # # 存储到数据库
    # # 存标签
    # print('insert tags begin...')
    # for idx in range(start+1,start+len(alltags)):
    #     print(alltags[idx])
    #     c.execute('insert into [BX-Tags](ID,Name,0) values({0},\'{1}\')'.format(idx,alltags[idx]))
    # conn.commit()
    # print('insert tags end.')

    # 存书和标签的对应关系
    # print('insert book and tags begin...')
    # for isbn in bookTags:
    #     print(isbn+':'+str(bookTags[isbn]))
    #     for tagid in bookTags[isbn]:
    #         print(tagid)
    #         c.execute('insert into [BX-Book-Tags](ISBN,[Tag-ID],[Rate]) values(\'{0}\',{1},0)'.format(isbn,tagid))
    # conn.commit()
    # print('insert book and tags end')
    
    print('fail isbn:'+str(failISBN))
    if len(failISBN)>0:
        with open(os.path.join(p,'../Data/failISBN.txt'),mode='a',encoding='utf-8',errors='ignore') as f:
            f.write(str(failISBN))
    

    # 如果还有，那么继续执行
    if begin<max and not invalid:
        genBash(begin+step,step,max)
    else:
        if invalid and Api.idx<len(Api.urls):
                sem.acquire()
                Api.idx+=1
                print('---------------------------------------------use idx:' + str(Api.idx)+'---------------------------------------------')
                sem.release()
                genBash(begin+step, step, max)
        else:
            try:
                conn.close()
            finally:
                print('conn closed')

# genBash(0,1,10000)
def do(start,max):
    sstep=30
    t = threading.Thread(target=genBash, args=(start, sstep,max))
    t.start()

threadNum=5
for i in range(threadNum):
    #pass
    # 每个线程处理的个数
    area = int(maxRowId/threadNum)
    do(i*area,(i+1)*area)


# conn.close()
