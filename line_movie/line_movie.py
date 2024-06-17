import requests
from bs4 import BeautifulSoup
import pandas as pd

data_list = []
def fetch_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    movies = soup.find_all("div", class_ = "detailListItem-details")
    for movie in movies:
        # 名稱
        name = movie.find("div", class_ = "detailListItem-titles")
        name = name.h2.text.strip()
        # 時長及上映時間
        tmp = movie.find_all("span", class_ = "text--ellipsis1")
        tmp2 = tmp[1].text.strip().replace("• ", "").replace("上映", "")
        date = ""
        time = ""
        for i in range(6):
            time += tmp2[i]
        for j in range(7, 18):
            date += tmp2[j]
        # 評分
        rating = movie.find("span", class_ = "iconInfo-text")
        rating = rating.text.strip()
        # 分類
        if len(tmp) == 3:
            category = tmp[2].text.strip().replace("• ", "")
        else:
            category = "尚未分類"
        # 分級
        level = movie.find("span", class_ = "glnBadge-text")
        level = level.text.strip()
        data_list.append([name, time, date, rating, category, level])
    print(data_list)

url = "https://today.line.me/tw/v2/movie/incinemas/playing"
fetch_data(url)

df = pd.DataFrame(data_list, columns=["電影名稱", "時長", "上映時間", "評分", "分類", "分級"])
df.to_excel("movie_online.xlsx", index=False, engine="openpyxl")
print("資料轉換xlsx成功")
