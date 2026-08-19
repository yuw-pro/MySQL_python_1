from douban_hepler import DoubanHelper
from SQL_helper import MySQLHelper

class DoubanFilms2:
    def __init__(self, pages=4, database = "douban"):
        self.pages = pages
        self.database = database
        self.douban = DoubanHelper()
        self.db = MySQLHelper(database = self.database)
    def fetch_all_films(self):
        self.films = self.douban.fetch_all(self.pages)
        if not self.films:
            raise RuntimeError('失败')
    def insert_all_films(self):
        try:
            self.db.connect()
            self.db.execute_query("TRUNCATE TABLE douban_films")
            for m in self.films:
                self.db.execute_query(
                    "INSERT INTO douban_films (rank_no, title, director, actors, genre, release_date, country, rating, review_count, film_url) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (m["rank_no"], m["title"], m["director"], m["actors"], m["genre"], m["release_date"], m["country"], m["rating"], m["review_count"], m["film_url"]))
        finally:
            self.db.close_connection()
        print('完成')
    def run(self):
        self.fetch_all_films()
        self.insert_all_films()
if __name__ == "__main__":
    DoubanFilms2().run()

