class getEM():
    def __init__(self, closeDict):
        self.closeDict = closeDict

    def getEMAtoday12(self, closeDict):
        EMA12 = {'date': [], 'close': []}
        for i in range(len(closeDict['close'])):
            if i == 0:
                EMA12['close'].append(closeDict['close'][0])
                EMA12['date'].append(closeDict['date'][0])
            else:
                EMA12['close'].append(2 / 13 * float(closeDict['close'][i])
                                      + 11 / 13 * float(EMA12['close'][i - 1]))
                EMA12['date'].append(closeDict['date'][i])
        return EMA12

    def getEMAtoday26(self, closeDict):
        EMA26 = {'date': [], 'close': []}
        for i in range(len(closeDict['close'])):
            if i == 0:
                EMA26['close'].append(closeDict['close'][0])
                EMA26['date'].append(closeDict['date'][0])
            else:
                EMA26['close'].append(2 / 27 * float(closeDict['close'][i])
                                      + 25 / 27 * float(EMA26['close'][i - 1]))
                EMA26['date'].append(closeDict['date'][i])
        return EMA26

    def getDEA(self, dif):
        dea = {'date': [], 'value': []}
        for i in range(len(dif['value'])):
            if i == 0:
                dea['value'].append(dif['value'][0])
                dea['date'].append(dif['date'][0])
            else:
                dea['value'].append(2 / 10 * float(dif['value'][i])
                                    + 8 / 10 * float(dea['value'][i - 1]))
                dea['date'].append(dif['date'][i])
        return dea

    def getDIF(self, closeDict):
        ema12 = self.getEMAtoday12(closeDict)
        ema26 = self.getEMAtoday26(closeDict)
        dif = {'date': [], 'value': []}
        for i in range(len(ema12['close'])):
            dif['value'].append(float(ema12['close'][i])
                                - float(ema26['close'][i]))
            dif['date'].append(ema12['date'][i])
        return dif
