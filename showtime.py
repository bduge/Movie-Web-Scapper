from pandas import DataFrame
import urllib.request
from bs4 import BeautifulSoup

imdb = "https://www.imdb.com/showtimes/location?ref_=sh_lc"
page = urllib.request.urlopen(imdb)
soup = BeautifulSoup(page, 'html.parser')

movies = []
ratings = []
runtime = []
release = []


def get_year(s):
    return s[:4]


movies_list = soup.find_all('div', attrs={'class': 'hidden inline-sort-params'})

for movie in movies_list:
    a = movie.find('span', attrs={'name': 'alpha'}).attrs['data-value']
    b = movie.find('span', attrs={'name': 'user_rating'}).attrs['data-value']
    c = movie.find('span', attrs={'name': 'runtime'}).attrs['data-value']
    d = movie.find('span', attrs={'name':'release_date'}).attrs['data-value']
    year = get_year(d)
    movies.append(a)
    ratings.append(b)
    runtime.append(c)
    release.append(year)


df = DataFrame({'Movies Playing': movies, 'Rating': ratings,
                'Runtime (min)': runtime, 'Release Year': release})
try:
    df.to_excel('showtimes.xlsx', sheet_name='sheet1', index=False)
except PermissionError:
    print("There was an error creating the spreadsheet, please make sure"
          " the file is not currently open.")








