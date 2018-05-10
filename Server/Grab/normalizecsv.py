import csv
import os
import sqlite3


conn=sqlite3.connect('../Data/Book_db.db')
c=conn.cursor()

path = os.path.join('../Data')

def dealOnefile(file):
    with open(os.path.join(path,file+'.csv'),mode='r',encoding='utf-8',errors='ignore') as ofile:
        with open(os.path.join(path,file+'-n.csv'),mode='w',encoding='utf-8',errors='igore',newline='') as nfile:
            fieldnames=[]
            nWriter = None
            executeSql= 'insert into '+ file
            oReader= ofile.readlines() #csv.reader(ofile)
            acc=0
            for rate in oReader:
                rrow=rate.split(';')
                if acc==0:                    
                    fieldnames = list(map(lambda x:x.replace('"', '').replace('\n','').replace('NULL',''), rrow))
                    nWriter=csv.DictWriter(nfile, fieldnames=fieldnames)
                    nWriter.writeheader()
                    acc=1
                    continue
                if len(rrow) < len(fieldnames):
                    continue

                # executeSql+= ','.join(rrow) +')'
                # print(executeSql)
                # c.execute(executeSql)
                # break
                o=dict()

                for i in range(len(fieldnames)):
                    o[fieldnames[i]] = rrow[i].replace('\n','').replace('NULL','')
                
                nWriter.writerow(o)
            print(file+',done!')

                
# dealOnefile('BX-Books')
dealOnefile('BX-Users')
# dealOnefile('BX-Book-Ratings')
