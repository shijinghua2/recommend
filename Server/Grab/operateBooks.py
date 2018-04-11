import csv
import os

rateDict = {}


path = os.path.join('../Data')
#path = "E:\git\douban\Server\Data"
with open(os.path.join(path, 'BX-Book-ratings.csv'), mode="r", encoding='utf-8', errors='ignore') as ratefile:
    rReader = csv.reader(ratefile)
    acc = 0
    # 遍历评分表，取出所有的评分
    for rate in rReader:
        rrow=rate[0].split(';')
        isbn=rrow[1]
        # 如果是第一行 或者 没有评分项，则跳过
        if acc == 0 or len(rrow) < 3:
            acc = 1
            continue
        brate = int(rrow[2].replace('"', ''))
        if brate == 0 or brate is None:
            continue
        if isbn in rateDict:
            if rateDict[isbn] is None:
                rateDict[isbn] = [brate]
            else:
                rateDict[isbn] = rateDict[isbn].append(brate)
        else:
            rateDict[isbn]=[brate]
    # 遍历评分数字典
    for rkey in rateDict.keys():
        if rateDict[rkey] == None:
            rateDict[rkey] = 0.0
        else:
            rateDict[rkey] = sum(rateDict[rkey]) / len(rateDict[rkey])
    #将平均分写入新表中
    headers = ['ISBN','AverageRating']
    with open(os.path.join(path, 'BX-Book-averageRatings.csv'), mode="w", encoding='utf-8', errors='ignore', newline='') as averageratingfile:
        aWriter = csv.DictWriter(averageratingfile, headers)
        aWriter.writeheader()
        b = sorted(rateDict.items(),key= lambda x:x[1] ,reverse=True)        
        c = list(map(lambda x: b[x], range(100)))
        for rrkey in c:
            aWriter.writerow({'ISBN': rrkey[0], 'AverageRating': rrkey[1]})

        


