import requests
from bs4 import BeautifulSoup
import os

def download_image(url, save_path):
    print(f"正在下載圖片:{url}")
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print("-" * 30)

def main():
    url = "https://www.ptt.cc/bbs/Beauty/M.1713479867.A.644.html"
    headers = {"Cookie": "over18=1",
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
            }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    
    # 抓標題
    spans = soup.find_all("span", class_ = "article-meta-value")
    # print(spans)
    title = spans[2].text

    # 建立標題資料夾
    dir_name = f"images/{title}"
    if not os.path.exists(dir_name): 
        os.makedirs(dir_name)

    # 找到網頁中所有圖片
    links = soup.find_all("a")
    allow_file_type = ["jpg", "jpeg", "png", "gif"]
    for link in links:
        href = link.get("href")
        if not href:
            continue
        file_name = href.split("/")[-1]
        extension = href.split(".")[-1].lower()
        if extension in allow_file_type:
            print(f"file type:{extension}")
            print(f"url:{href}")
            download_image(href, f"{dir_name}/{file_name}")
    
# 如果是圖片下載
if __name__ == "__main__":
    main()