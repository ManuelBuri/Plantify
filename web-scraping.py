import requests
from bs4 import BeautifulSoup as bs

page = requests.get('http://www.dennerle.com/de/service/pflanzendatenbank')
page.status_code
print(page.status_code)

data = page.text

page_soup = bs(data, 'html.parser')
#print(page_soup.prettify())
#print(list(page_soup.children))

name = page_soup.select('.description h4')
name_clean = page_soup.get_text()

lat_names = []
wuchshoehe = []
eignung = []
familie = []
vermehrung = []
ph = []
herkunft = []
typ = []
gattung = []
geschwindigkeit = []
wasserhaerte = []
hinweise = []

for t in page_soup.find_all('div', class_='description'):
    value = t.select('h4')[0].text
    lat_names.append(value)
    value = t.find_all('td')[0].text
    wuchshoehe.append(value)
    value = t.find_all('td')[1].text
    herkunft.append(value)
    value = t.find_all('td')[1].text
    eignung.append(value)
    value = t.find_all('td')[2].text
    typ.append(value)
    value = t.find_all('td')[3].text
    familie.append(value)
    value = t.find_all('td')[4].text
    gattung.append(value)
    value = t.find_all('td')[5].text
    vermehrung.append(value)
    value = t.find_all('td')[6].text
    geschwindigkeit.append(value)
    value = t.find_all('td')[7].text
    ph.append(value)
    value = t.find_all('td')[8].text
    wasserhaerte.append(value)
    value = t.find_all('p')
    hinweise.append(value)

print(lat_names)
print(wuchshoehe)
print(eignung)
print(familie)
print(vermehrung)
print(ph)
print(herkunft)
print(typ)
print(gattung)
print(geschwindigkeit)
print(wasserhaerte)
print(hinweise)


