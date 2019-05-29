# 判断各种走势
import tushare as ts
import threading

lock = threading.Lock()

sumCode = 0
succ = 0
succ3 = 0
succ5 = 0
sumCode2 = 0
defe = 0
defe3 = 0
defe5 = 0
highestList = {'days': [i for i in range(1, 40)], 'times': [0 for i in range(1, 40)]}
lowestList = {'days': [i for i in range(1, 40)], 'times': [0 for i in range(1, 40)]}


class Judge(object):

    def judgeTwiceCross(self, code, macdSum, dif, codeDict):

        global sumCode
        global succ
        global succ3
        global succ5
        global sumCode2
        global defe
        global defe3
        global defe5
        for i in range(1, len(macdSum['value']) - 3):
            if macdSum['value'][i] > 0 and macdSum['value'][i + 1] < 0:  # 红绿
                date1 = macdSum['date'][i]
                date2 = macdSum['date'][i + 2]
                date3 = macdSum['date'][i + 3]
                dif1 = dif['value'][dif['date'].index(date1)]
                dif2 = dif['value'][dif['date'].index(date2)]
                lock.acquire()
                if 0.5 < dif2 and 0.5 < dif1 and self.judgeTopDivergence(codeDict, dif1, dif2, date1, date2):
                    print('出现高位二次死叉，死叉出现的时间分别为：', date1, ",", date2, "。\n预计在", date2, ",该只股票会连续下跌")
                    sumCode2 += 1
                    ratio2, lowestDays = self.scoring2(code, date2, date3)
                    if ratio2 <= 1:
                        defe += 1
                    if ratio2 <= 0.97:
                        defe3 += 1
                    if ratio2 <= 0.95:
                        defe5 += 1
                    lowestList['times'][lowestDays] += 1
                lock.release()

            if macdSum['value'][i] < 0 and macdSum['value'][i + 1] > 0:  # 绿红
                date1 = macdSum['date'][i]
                date2 = macdSum['date'][i + 2]
                date3 = macdSum['date'][i + 3]
                dif1 = dif['value'][dif['date'].index(date1)]
                dif2 = dif['value'][dif['date'].index(date2)]
                lock.acquire()
                if dif1 + 0.2 < dif2 < 0 and self.judgeBottomDivergence(codeDict, dif1, dif2, date1, date2):  # 低位二次金叉
                    print('出现低位二次金叉，金叉出现的时间分别为：', date1, ",", date2,
                          "。\n预计在", date2, ",该只股票会连续上涨")
                    sumCode += 1
                    ratio, highestDays = self.scoring(code, date2, date3)
                    if ratio >= 1:
                        succ += 1
                    if ratio >= 1.03:
                        succ3 += 1
                    if ratio >= 1.05:
                        succ5 += 1
                    highestList['times'][highestDays] += 1
                lock.release()

    def judgeTopDivergence(self, data, dif1, dif2, date1, date2):  # 判断顶背离
        if dif1 > dif2 and data['high'][data['date'].index(date1)] < data['low'][data['date'].index(date2)]:
            print("出现顶背离，", end="")
            return 1

    def judgeBottomDivergence(self, data, dif1, dif2, date1, date2):  # 判断底背离
        if dif1 < dif2 and data['low'][data['date'].index(date1)] > data['high'][data['date'].index(date2)]:
            print("出现底背离，", end="")
            return 1

    def scoring(self, code, date2, date3):
        data = ts.get_hist_data(code, start=str(date2), end=str(date3))
        highestClose = 0
        highestDays = 0
        if data is not None:
            for i in range(len(data) - 1):
                if data['close'][i] > highestClose:
                    highestClose = data['close'][i]
                if data['close'][i] > data['close'][i + 1]:  # 按日期倒序排列
                    highestDays += 1
            ratio = highestClose / data['close'][len(data['close']) - 1]
            return ratio, highestDays  # 最大涨幅

    def scoring2(self, code, date2, date3):
        data = ts.get_hist_data(code, start=str(date2), end=str(date3))
        lowestClose = 1000
        lowestDays = 0
        if data is not None:
            for i in range(len(data['close']) - 1):
                if data['close'][i] < lowestClose:
                    lowestClose = data['close'][i]
                if data['close'][i] < data['close'][i + 1]:
                    lowestDays += 1

            ratio2 = lowestClose / data['close'][len(data['close']) - 1]
            return ratio2, lowestDays  # 最大跌幅
