import unittest
from douban_films2 import DoubanFilms2

class TestDoubanFilms2(unittest.TestCase):

    def test_fetch_all_films(self):
        f1 = DoubanFilms2(pages=4)
        f1.fetch_all_films()
        self.assertEqual(len(f1.films), 100)
        self.assertEqual(f1.films[0]['rank_no'], 1)
        self.assertEqual(f1.films[0]['title'], '肖申克的救赎')
    def test_fetch_all_films_fail(self):
        f2 = DoubanFilms2(pages=0)
        with self.assertRaises(RuntimeError):
            f2.fetch_all_films()
    def test_insert_all_films(self):
        f3 = DoubanFilms2(pages=4)
        f3.fetch_all_films()
        f3.insert_all_films()
        f3.db.connect()
        rows = f3.db.query_all("douban_films")
        self.assertEqual(len(rows), 100)
if __name__ == "__main__":
    unittest.main()
