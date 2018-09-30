
import urllib.request
from bs4 import BeautifulSoup

imdb = "https://www.imdb.com/showtimes/location?ref_=sh_lc"
page = urllib.request.urlopen(imdb)
soup = BeautifulSoup(page, 'html.parser')

movies_list = soup.find_all('div', attrs={'class': 'hidden inline-sort-params'})

for movie in movies_list:
    a = movie.find('span', attrs={'name': 'alpha'}).attrs['data-value']
    print(a)

