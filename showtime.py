
import urllib.request
from bs4 import BeautifulSoup

imdb = "https://www.imdb.com/showtimes/location?ref_=sh_lc"
page = urllib.request.urlopen(imdb)
soup = BeautifulSoup(page,'html.parser')
