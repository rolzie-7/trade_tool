import yfinance as yf
import mplfinance as mpf
import time
import matplotlib.pyplot as plt

# 开启交互模式
plt.ion()

while True:
    try:
        # 获取最新的黄金期货数据
        gold = yf.Ticker("GC=F")
        data = gold.history(period="1d", interval="1m")

        # 获取最近 60 根 K 线
        recent_data = data.tail(60)

        # 关闭上一个图像窗口（避免多窗口堆积）
        plt.close('all')

        # 创建新的图像对象
        fig, axes = mpf.plot(recent_data,
                             type='candle',
                             style='charles',
                             title='[实时] 黄金期货 1分钟K线图 (GC=F)',
                             ylabel='Price (USD)',
                             volume=True,
                             mav=(5, 10),
                             returnfig=True,
                             tight_layout=True)

        # 显示图像（不阻塞主线程）
        plt.show(block=False)

        # 等待 60 秒
        plt.pause(60)

    except Exception as e:
        print("发生错误：", e)
        time.sleep(60)
