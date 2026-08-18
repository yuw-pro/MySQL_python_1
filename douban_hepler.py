from bs4 import BeautifulSoup
import requests

class DoubanHelper:
    def __init__(self, url='', page=1):
        self.url = url
        self.page = page
        self.headers = {
            "User-Agent": "Mozilla/5.0"}
        self.rank_no = (page - 1) * 25
        self.response = None
        self.soup = None
        self.information = None
        self.film_data = []
    def fetch_data(self):
        self.response = requests.get(self.url, headers=self.headers)
        if self.response.status_code == 200:
            self.soup = BeautifulSoup(self.response.text, "html.parser")
            return self.soup
        else:
            print(f"Failed to fetch data. Status code: {self.response.status_code}")
            return None
        #先尝试列表一个个全取
    def fetch_info(self):
        self.information = self.soup.find_all("div", class_="info")
        return self.information
    #寻找review
    def fetch_reviews(self, film_info):
        bd_dives = film_info.find("div", class_='bd')
        if bd_dives:
            for span in bd_dives.find_all("span"):
                if '评价' in span.get_text(strip=True):
                    return int(span.get_text(strip=True).replace('人评价', '').strip())
        return None 
    def split_text(self, film_info):
        self.actor = None
        self.director = None
        self.release = None
        self.genre = None
        self.country = None
        all_text = film_info.find('p').get_text('\n', strip=True).replace('\xa0', ' ')
        lines = all_text.split('\n')
        line1 = lines[0]
        if '主演' in line1:
            self.actor = line1.split('主演:', 1)[1].strip()
            self.director = line1.split('主演', 1)[0].replace('导演:', '').strip()
        else:
            self.actor = None
            self.director = line1.replace('导演:', '').strip()
        if len(lines) > 1:                      
            parts = lines[1].split('/')
            release_raw = parts[0].strip() 
            self.release =  release_raw.split('(', 1)[0]
            # self.relase = parts[0].
            if len(parts) > 2:
                self.country = parts[-2].strip()
                self.genre = parts[-1].strip()        
        return self.actor, self.director, self.release, self.country, self.genre
    def fetch_film_info(self, info):
        #for info in self.information:
        for film_info in info:
            self.rank_no += 1
            title = film_info.find('span', class_='title').get_text(strip=True)
            actor, director, release, country, genre = self.split_text(film_info)
            rating = film_info.find('span', class_='rating_num', 
                        property="v:average").get_text(strip=True)
            review = self.fetch_reviews(film_info)
            film_url = film_info.find("a", href=True).get("href")
            self.film_data.append({
                "rank_no": self.rank_no,
                "title": title,
                "director": director,
                "actors": actor,
                "genre": genre,
                "country": country,
                "release_date": release,
                "rating": float(rating),
                "review_count": review,
                "film_url": film_url
            })
        return self.film_data
    def fetch_all(self, pages):
        self.film_data = []
        self.rank_no = 0
        for page in range(1,pages+1):
            self.url = f"https://movie.douban.com/top250?start={(page-1)*25}&filter="
            self.fetch_data()
            self.information = self.fetch_info()
            self.fetch_film_info(self.information)
        return self.film_data
    
        