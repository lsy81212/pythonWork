class Macd(object):
    def __init__(self, dif, dea, closeDict):
        self.dif = dif
        self.dea = dea
        self.closeDict = closeDict

    def getMACD(self, dif, dea, closeDict):
        macd = {'date': [], 'value': []}
        for i in range(len(dif['date'])):
            macd['date'].append(closeDict['date'][i])
            macd['value'].append((dif['value'][i] - dea['value'][i]) * 2)
        return macd

    def calculateMACD(self, macd):
        macdSum = {'date': [], 'value': []}
        j = 1
        macdSum['date'].append(macd['date'][0])
        macdSum['value'].append(macd['value'][0])
        for i in range(1, len(macd['value']) - 1):
            if macd['value'][i] * macd['value'][i + 1] < 0:
                macdSum['date'].append(macd['date'][i])
                macdSum['value'].append(sum(macd['value'][j:i]))
                j = i + 1
        macdSum['date'].append(macd['date'][len(macd['date']) - 1])
        macdSum['value'].append(sum(macd['value'][j:len(macd['value'])]))
        return macdSum
