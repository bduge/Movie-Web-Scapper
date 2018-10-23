from pandas import DataFrame
import urllib.request
from bs4 import BeautifulSoup

postcode = input("Please enter your postal code so we may show you relevant showtime information (no spaces)")

# initializes variables used for beautifulsoup
imdb = "https://www.imdb.com/showtimes/location/CA/" + postcode + "?ref_=sh_lc"
page = urllib.request.urlopen(imdb)
soup = BeautifulSoup(page, 'html.parser')

# initializes arrays used for storing scrapped information
movies = []
review = []
runtime = []
release = []
rating = []
genre = []
showtimes = []


def get_year(s):  # formats date string to return the year
    return s[:4]


def get_time(s):  # formats time string to return the length of movie in minutes
    return s[-5:]


def get_selection():  # helper function for the user to select a movie they're interested in watching
    try:
        s = int(input())
        return s
    except ValueError:
        print("")


movies_list = soup.find_all('div', attrs={'class': 'lister-item mode-grid'})

for movie in movies_list:   # uses a loop to extract the information of a movie for all movies playing
    a = movie.find('span', attrs={'name': 'alpha'}).attrs['data-value']
    b = movie.find('span', attrs={'name': 'user_rating'}).attrs['data-value']
    c = movie.find('span', attrs={'name': 'runtime'}).attrs['data-value']
    d = movie.find('span', attrs={'name':'release_date'}).attrs['data-value']

    try:
        e = movie.find('span', attrs={'class': 'certificate'}).string
    except AttributeError:
        e = ""

    f = movie.find('span', attrs={'class': 'genre'}).string.strip()
    g = movie.find('div', attrs={'class': 'title'}).a.get('href')
    year = get_year(d)

    movies.append(a)
    review.append(b)
    runtime.append(c)
    release.append(year)
    rating.append(e)
    genre.append(f)
    showtimes.append("https://www.imdb.com"+g)  # formats the string to produce a url based on the link within html file

# provides user a list of movies playing and a method of inputting their selection
print("Here are the movies playing near you: \n")

for x in range(0, len(movies)):
    print(str(x+1) + ". {}  {}/10  Runtime: {} \n    Release Year: {}  Genre: {} {}\n"
          .format(movies[x], review[x], runtime[x], release[x], genre[x], rating[x]))

print("Please select a movie: ")

selection = get_selection()
while not(isinstance(selection, int)) or selection < 1 or selection > len(movies):
    print("Your selection was not valid, please try again: ")
    selection = get_selection()


# Creates new soup to access more detailed information about movie after user has made their selection
detailedMovie = showtimes[selection-1]
page2 = urllib.request.urlopen(detailedMovie[:47] + "CA/" + postcode)
soup2 = BeautifulSoup(page2, 'html.parser')


theaters_list = soup2.findAll('div', attrs={'class': 'list detail'})
times = []
print("Showtimes for " + movies[selection-1] + " : \n")

# Finds all the theaters in local area of user
for theater in theaters_list:
    odd = theater.findAll('div', attrs={'class', 'list_item odd'})
    even = theater.findAll('div', attrs={'class', 'list_item even'})

    for x in odd:
        print(x.find('span', attrs={'itemprop': 'name'})
              .find(text=True, recursive=False))
        print(x.find('span', attrs={'itemprop': 'streetAddress'}).string)
        times = x.findAll('meta', attrs={'itemprop': 'startDate'})
        for y in times:
            print(get_time(y.attrs['content']) + '  ', end="", flush=True)
        print('\n')

    for x in even:
        print(x.find('span', attrs={'itemprop': 'name'})
              .find(text=True, recursive=False))
        print(x.find('span', attrs={'itemprop': 'streetAddress'}).string)
        times = x.findAll('meta', attrs={'itemprop': 'startDate'})
        for y in times:
            print(get_time(y.attrs['content']) + '  ', end="", flush=True)
        print('\n')

df = DataFrame({'Movies Playing': movies, 'Rating': review,
                'Runtime (min)': runtime, 'Release Year': release})
try:
    df.to_excel('showtimes.xlsx', sheet_name='sheet1', index=False)
except PermissionError:
    print("There was an error creating the spreadsheet, please make sure"
          " the file is not currently open.")











