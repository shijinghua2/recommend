import csv
import os
import sqlite3

conn=sqlite3.connect('../Data/Book.db')
c=conn.cursor()

rateDict = {}

cursor=c.execute('select [User-ID],[ISBN],[Book-Rating] from [BX-Book-Ratings]')
for row in cursor:
    isbn=row[1]
    rate=int(row[2])
    if rate==0:
        continue
    if isbn in rateDict:  
        rateDict[isbn].append(rate)
    else:
        rateDict[isbn] = [rate]

# 遍历评分数字典
for rkey in rateDict.keys():
    if rateDict[rkey] == None:
        rateDict[rkey] = 0.0
    else:
        rateDict[rkey] = sum(rateDict[rkey]) / len(rateDict[rkey])
    
    sql = 'update [BX-Books] set [Book-Avg-Rating]={0} where [ISBN]=\'{1}\''.format(rateDict[rkey], rkey.replace('"','').replace("'",''))
    
    c.execute(sql)
conn.commit()
conn.close()


        


