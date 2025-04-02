import yfinance as yf
import pandas as pd
import time
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np
import sys

# 设置图表风格，调整主图/副图比例
custom_style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 10})

all_data = pd.DataFrame()

try:
    while True:
        gold = yf.Ticker("GC=F")
        data = gold.history(period="1d", interval="1m")

        if data.empty:
            print("[Warning] No data fetched.")
            time.sleep(60)
            continue

        print("Latest prices:")
        print(data.tail(2))

        new_data = data[~data.index.isin(all_data.index)]
        if not new_data.empty:
            all_data = pd.concat([all_data, new_data])
            print("New row added:")
            print(new_data.tail(1))

        if len(all_data) >= 20:
            median_price = all_data['Close'].median()
            filtered_data = all_data[all_data['Close'] > median_price * 0.9]

            fig, _ = mpf.plot(
                filtered_data.tail(60),
                type='candle',
                style=custom_style,
                ylabel='USD',
                volume=True,
                mav=(5, 10),
                figratio=(16, 9),
                figscale=1.8,
                returnfig=True,
                tight_layout=True,
                panel_ratios=(10, 1)  
            )
            fig.canvas.manager.set_window_title("GC=F Gold Futures - Real-Time K Line 10min delay")


            plt.show(block=True)
            print("Chart window closed. Program exits.")
            break

        time.sleep(60)

except KeyboardInterrupt:
    print("\nUser interrupted. Exiting cleanly.")
    sys.exit(0)

except Exception as e:
    print("Error:", e)
    time.sleep(60)
