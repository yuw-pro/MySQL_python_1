from douban_hepler import DoubanHelper
from SQL_helper import MySQLHelper

douban = DoubanHelper()
films_100 = douban.fetch_all(4)

db = MySQLHelper(database="douban")
db.connect()
db.execute_query("TRUNCATE TABLE douban_films")
for m in films_100:
    db.execute_query(
        "INSERT INTO douban_films (rank_no, title, director, actors, genre, release_date, country, rating, review_count, film_url) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (m["rank_no"], m["title"], m["director"], m["actors"],
         m["genre"], m["release_date"], m["country"], m["rating"],
         m["review_count"], m["film_url"])
    )
db.close_connection()
print("数据插入完成")