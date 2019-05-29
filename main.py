import tushare as ts
import getEMA as EMA
import calMACD as cM
import paint as p
import csv
import judgeTrend
import cod as c
import time, threading
import os

lock = threading.Lock()


def getCodeDict(file):
    codeDict = {'date': [], 'close': [], 'high': [], 'low': []}
    with open(file, 'r', encoding="utf-8") as f:
        lines = csv.reader(f)
        for line in lines:
            codeDict['date'].append(line[0])
            codeDict['close'].append(line[1])
            codeDict['high'].append(line[2])
            codeDict['low'].append(line[3])

    del codeDict['date'][0]
    del codeDict['close'][0]
    del codeDict['high'][0]
    del codeDict['low'][0]

    codeDict['date'].reverse()
    codeDict['close'].reverse()
    codeDict['high'].reverse()
    codeDict['low'].reverse()
    return codeDict


su = 0


def loop(codeList, k):
    global su
    for i in range(len(codeList)):
        print("当前计算线程", k, "的第", i, "支股票")
        # data = ts.get_hist_data(codeList[i], start='2018-06-01', end='2019-05-20')
        # if data is None:
        #     continue
        # data.to_csv('d:/day/'+str(k)+'/'+str(i)+'-'+str(codeList[i])+'.csv', columns=['close', 'high', 'low'])
        info = 'd:/day/' + str(k) + '/' + str(i) + '-' + str(codeList[i]) + '.csv'

        if not os.path.exists(info):
            continue
        codeDict = getCodeDict(info)
        if len(codeDict['date']) < 100:
            continue
        lock.acquire()
        su += 1
        lock.release()
        e = EMA.getEM(closeDict=codeDict)
        dif = e.getDIF(codeDict)
        dea = e.getDEA(dif)
        # p.draw(dif, dea)  # 画图
        c = cM.Macd(dif=dif,dea=dea,closeDict=codeDict)
        macd = c.getMACD(dif, dea, codeDict)
        macdSum = c.calculateMACD(macd)
        j = judgeTrend.Judge()
        j.judgeTwiceCross(codeList[i], macdSum, dif, codeDict)


if __name__ == '__main__':
    start = time.time()
    codeList = c.code  # 全部股票代码
    codeLen = len(codeList)
    baseLen = int(len(codeList) / 4)
    list1 = [codeList[i] for i in range(baseLen)]
    list2 = [codeList[i] for i in range(baseLen, baseLen * 2)]
    list3 = [codeList[i] for i in range(baseLen * 2, baseLen * 3)]
    list4 = [codeList[i] for i in range(baseLen * 3, codeLen)]
    t1 = threading.Thread(target=loop, args=(list1, 1))
    t2 = threading.Thread(target=loop, args=(list2, 2))
    t3 = threading.Thread(target=loop, args=(list3, 3))
    t4 = threading.Thread(target=loop, args=(list4, 4))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    lowestList = judgeTrend.lowestList
    defe = judgeTrend.defe
    defe3 = judgeTrend.defe3
    defe5 = judgeTrend.defe5
    sumCode2 = judgeTrend.sumCode2
    print("二次死叉后下跌的几率为：", defe / sumCode2)
    print("下跌幅度大于3%的几率为：", defe3 / sumCode2)
    print("下跌幅度大于5%的几率为：", defe5 / sumCode2)
    print("下跌峰值分布:", end="")
    print(lowestList)
    p.draw2(lowestList['times'])

    highestList = judgeTrend.highestList
    succ = judgeTrend.succ
    succ3 = judgeTrend.succ3
    succ5 = judgeTrend.succ5
    sumCode = judgeTrend.sumCode
    print("二次金叉后上涨的几率为：", succ / sumCode)
    print("上涨幅度大于3%的几率为：", succ3 / sumCode)
    print("上涨幅度大于5%的几率为：", succ5 / sumCode)
    print("上涨峰值分布:", end="")
    print(highestList)
    p.draw2(highestList['times'])
    print(su)
    end = time.time()
    print("运行耗时：", end - start)
