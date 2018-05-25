import requests
from bs4 import BeautifulSoup as bs

page = requests.get('http://www.dennerle.com/de/service/pflanzendatenbank')
page.status_code
print(page.status_code)

page_soup = bs(page.content, 'html.parser')
#print(page_soup.prettify())
print(list(page_soup.children))