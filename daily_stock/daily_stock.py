import requests
import pandas as pd

url = "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL"

response = requests.get(url)
if response.status_code ==200:
    data = response.json()
    # print(data)
    stock_list = []
    for i in range(len(data)):
        stock_data = [
            data[i]['Code'], 
            data[i]['Name'],
            data[i]['TradeVolume'],
            data[i]['TradeValue'],
            data[i]['OpeningPrice'],
            data[i]['HighestPrice'],
            data[i]['LowestPrice'],
            data[i]['ClosingPrice'],
            data[i]['Change'],
            data[i]['Transaction']
        ]
        stock_list.append(stock_data)
    # print(stock_list)
    df = pd.DataFrame(stock_list, columns=["股票代碼", "公司名稱", "成交股數", "成交金額", "開盤價", "最高價", "最低價", "收盤價", "漲跌價差", "成交筆數"])
    df.to_excel('daily_stock.xlsx', index=False, engine="openpyxl")
    print("Save successfully.")
else:
    print("無法擷取資料")