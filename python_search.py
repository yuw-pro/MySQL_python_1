import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from SQL_helper import MySQLHelper

load_dotenv()

class BaiduHotSearch:
    def __init__(self, database="baidu_hot_search_sql", top_n=10):
        self.url = "https://top.baidu.com/board?tab=realtime"
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.database = database
        self.top_n = top_n
        self.db = MySQLHelper(
            host="localhost",
            user="root",
            password=os.getenv("MySQL_password"),
            database=self.database
        )
        self.hot_items = []

    def fetch(self):
        response = requests.get(self.url, headers=self.headers, timeout=10)
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("div", class_="c-single-text-ellipsis")
        self.hot_items = [item.get_text(strip=True) for item in items[:self.top_n]]
        return self.hot_items

    def save_to_db(self):
        if not self.hot_items:
            print("没有可保存的热搜数据")
            return
        
        connection = self.db.connect()
        if connection and connection.is_connected():
            print("成功连接到数据库，正在写入数据...")
            try:
                for rank_no, title in enumerate(self.hot_items, start=1):
                    self.db.insert_hot_search(
                        rank_no, title, None, None, datetime.now()
                    )
                print(f"已成功插入前 {len(self.hot_items)} 条热搜数据。")
            finally:
                self.db.close_connection()
        else:
            print("数据库连接失败，跳过写入。")

    def run(self):
        print("=== 开始爬取百度热搜 ===")
        self.fetch()
        print(f"抓取到 {len(self.hot_items)} 条热搜:")
        for idx, title in enumerate(self.hot_items, 1):
            print(f"  {idx}. {title}")
        print("=== 正在保存至数据库 ===")
        self.save_to_db()
        print("=== 运行结束 ===")

if __name__ == '__main__':
    search = BaiduHotSearch()
    search.run()
