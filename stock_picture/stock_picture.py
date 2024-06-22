import yfinance as yf
import mplfinance as mpf
import requests
import pandas as pd

url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"
response = requests.get(url)
if response.status_code ==200:
    data = response.json()
    stock_list = []
    for i in range(len(data)):
        stock_list.append(data[i]['Code'])
    # print(stock_list)
else:
    print("無法擷取資料")

no = 0
while(no not in stock_list):
    no = input("請輸入欲查詢的股票代碼\n")
start = input("請輸入起始時間，範例：2024-01-01\n")
end = input("請輸入終止時間，範例：2024-06-22\n")
df = yf.download(f'{no}.tw', start, end) 
#繪製K線圖:candle 也就是我們常講的K線，平均移動線:mav繪製5、20日MA
mpf.plot(df, type='candle', mav=(5,20), volume=True, title=f'{no}.TW', savefig=f'{no}_plot.png')