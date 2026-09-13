from douban_hepler import DoubanHelper
from SQL_helper import MySQLHelper

class Douban_Films:
    def __init__(self, pages=4):
        self.pages = pages
        self.douban = DoubanHelper()
        self.db = MySQLHelper(database="douban")
        self.films = []

    def fetch_films(self):
        self.films = self.douban.fetch_all(self.pages)
        return self.films

    def insert_films(self):
        self.db.connect()
        try:
            self.db.execute_query("TRUNCATE TABLE douban_films")
            for m in self.films:
                self.db.execute_query(
                    "INSERT INTO douban_films (rank_no, title, director, actors, genre, release_date, country, rating, review_count, film_url) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (m["rank_no"], m["title"], m["director"], m["actors"],
                     m["genre"], m["release_date"], m["country"], m["rating"],
                     m["review_count"], m["film_url"])
                )
            print("数据插入完成")
        finally:
            self.db.close_connection()

    def run(self):
        self.fetch_films()
        self.insert_films()

if __name__ == '__main__':
    Douban_Films(pages=4).run()
