from douban_films2 import DoubanFilms2

def test_fetch_all_films():
    f1 = DoubanFilms2(pages=4)
    f1.fetch_all_films()
    assert len(f1.films) == 100
    assert f1.films[0]["rank_no"] == 1
    assert "title" in f1.films[0]
def test_fetch_all_films_fail():
    f2 = DoubanFilms2(pages=0)
    import pytest
    with pytest.raises(RuntimeError):
        f2.fetch_all_films()
def test_insert_all_films():
    f3 = DoubanFilms2(pages=4)
    f3.fetch_all_films()
    f3.insert_all_films()
    f3.db.connect()
    rows = f3.db.query_all("douban_films")
    assert len(rows) == 100
