from pandas import DataFrame
import urllib.request
from bs4 import BeautifulSoup

imdb = "https://www.imdb.com/showtimes/location?ref_=sh_lc"
page = urllib.request.urlopen(imdb)
soup = BeautifulSoup(page, 'html.parser')

movies = []
review = []
runtime = []
release = []
rating = []
genre = []
showtimes=[]


def get_year(s):
    return s[:4]


def get_selection():
    try:
        s = int(input())
        return s
    except ValueError:
        print("")


movies_list = soup.find_all('div', attrs={'class': 'lister-item mode-grid'})

for movie in movies_list:
    a = movie.find('span', attrs={'name': 'alpha'}).attrs['data-value']
    b = movie.find('span', attrs={'name': 'user_rating'}).attrs['data-value']
    c = movie.find('span', attrs={'name': 'runtime'}).attrs['data-value']
    d = movie.find('span', attrs={'name':'release_date'}).attrs['data-value']
    e = movie.find('span', attrs={'class': 'certificate'}).string
    f = movie.find('span', attrs={'class': 'genre'}).string.strip()
    g = movie.find('div', attrs={'class': 'title'}).a.get('href')
    year = get_year(d)

    movies.append(a)
    review.append(b)
    runtime.append(c)
    release.append(year)
    rating.append(e)
    genre.append(f)
    showtimes.append("https://www.imdb.com"+g)

print("Here are the movies playing near you: \n")
for x in range(0, len(movies)):
    print(str(x+1) + ". {}  {}/10  Runtime: {} \n    Release Year: {}  Genre: {}  {}\n"
          .format(movies[x], review[x], runtime[x], release[x], genre[x], rating[x]))

print("Please select a movie: ")
selection = get_selection()
while not(isinstance(selection, int)) or selection < 1 or selection > len(movies):
    print("Your selection was not valid, please try again: ")
    selection = get_selection()

detailedMovie = showtimes[selection-1]
page2 = urllib.request.urlopen(detailedMovie)
soup2 = BeautifulSoup(page2, 'html.parser')

print(soup2.prettify())

df = DataFrame({'Movies Playing': movies, 'Rating': review,
                'Runtime (min)': runtime, 'Release Year': release})
try:
    df.to_excel('showtimes.xlsx', sheet_name='sheet1', index=False)
except PermissionError:
    print("There was an error creating the spreadsheet, please make sure"
          " the file is not currently open.")












