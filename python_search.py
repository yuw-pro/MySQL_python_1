import requests

url1 = "https://top.baidu.com/board?tab=realtime"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response1 = requests.get(url1, headers=headers)
print(response1.status_code)

from bs4 import BeautifulSoup

soup1 = BeautifulSoup(response1.text, "html.parser")

print(soup1.title.string)
items = soup1.find_all("div", class_="c-single-text-ellipsis")
for item in items[:10]:
    print(item.get_text(strip=True))

from SQL_helper import MySQLHelper
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime

database1_baidu = MySQLHelper(host="localhost", 
user="root", password=os.getenv("MySQL_password"), 
database="baidu_hot_search_sql")
connection1 = database1_baidu.connect()
if connection1.is_connected():
    print("Connected to the database successfully.")
    rank_no = 0
    for item in items[:10]:
        rank_no += 1
        database1_baidu.insert_hot_search(
        rank_no, item.get_text(strip=True), None, None, datetime.now())
else:
    print("Error connecting to the database.")



