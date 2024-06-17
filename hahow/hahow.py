import requests
import pandas as pd

url = "https://api.hahow.in/api/products/search?category=COURSE&filter=PUBLISHED&limit=24&page=0&sort=TRENDING"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)
if response.status_code ==200:
    data = response.json()
    # print(data['data']['courseData']['products'])
    products = data['data']['courseData']['products']
    course_list = []
    for product in products:
        course_data = [
            product['title'], 
            product['averageRating'], 
            product['price'], 
            product['numSoldTickets']
        ]
        course_list.append(course_data)
    df = pd.DataFrame(course_list, columns=["課程名稱", "評價", "價格", "購買人數"])
    df.to_excel('course.xlsx', index=False, engine="openpyxl")
    print("Save successfully.")
else:
    print("無法取得網頁")
