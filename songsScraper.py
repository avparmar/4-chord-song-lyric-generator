from bs4 import BeautifulSoup
import urllib2
import re
import csv
from unidecode import unidecode

# by Aditya Parmar

url = "https://en.wikipedia.org/wiki/List_of_songs_containing_the_I%E2%80%93V%E2%80%93vi%E2%80%93IV_progression"

page = urllib2.urlopen(url)
parser = BeautifulSoup(page, 'html.parser')

the_table = parser.find_all('table')[0]


rows = the_table.find_all('tr')


# print the_table

myData = []

for row in rows:
    cells = row.find_all("td")
    if len(cells) > 0:
        if cells[1].find('a'):
            artist = cells[1].find_all('a')[0].text
        else:
            title = cells[1].text

        title = cells[0].text

        if title.find('[') > 0:
            title = title[0:title.find('[')]
        if title.find('(') > 0:
            title = title[0:title.find('(')]
        if artist.find('(') > 0:
            artist = artist[0:artist.find('(')]
        title = title.replace("\"","").replace(",","").replace("\'","")
        title = re.sub(r"\[.*\]\n", " ", unidecode(title))
        artist = re.sub(r"\[.*\]\n", " ", unidecode(artist))
        artist = artist.replace("!","")

        myData.append((title, artist))

with open('songsData.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    for title, artist in myData:
        writer.writerow([title, artist])