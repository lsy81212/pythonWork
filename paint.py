import matplotlib.pyplot as plt


def draw(dif, dea):
    # X轴，Y轴数据
    x = []
    y = []
    macd = []
    for i in range(len(dif['value'])):
        x.append(i)
        y.append(0)
        macd.append((dif['value'][i] - dea['value'][i]) * 2)
    macd2 = macd.copy()
    for i in range(len(macd)):
        if macd2[i] > 0:
            macd2[i] = 0
    plt.figure(figsize=(8, 4))  # 创建绘图对象
    plt.plot(x, dif['value'], "b--", linewidth=1)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.plot(x, dea['value'], "y--", linewidth=1)
    plt.plot(x, y, "black", linewidth=1)
    plt.bar(x, macd, alpha=0.9, width=0.6, facecolor='red')
    plt.bar(x, macd2, alpha=0.9, width=0.6, facecolor='green')
    plt.xlabel("Time(s)")  # X轴标签
    plt.ylabel("Volt")  # Y轴标签
    plt.title("Line plot")  # 图标题
    plt.show()  # 显示图

def draw2(data):
    plt.bar(range(len(data)), data)
    plt.show()  # 显示图
