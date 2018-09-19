import urllib2
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import pandas
import csv

# by Aditya Parmar

forma = "http://www.metrolyrics.com/{}-lyrics-{}.html"

songs = pandas.read_csv('songsData.csv')


allLyrics = []

for index, row in songs.iterrows():
    trueURL = forma.format(row['title'],row['artist'])
    trueURL = trueURL.replace(" ","-").lower()
    #print trueURL

    try: 
        page = urllib2.urlopen(trueURL)
        parser = BeautifulSoup(page, 'html.parser')


        lyrics = ""
        allVerses = parser.find_all('p', attrs={'class':'verse'})
        for verse in allVerses:
            lines = re.sub(r"\[.*\]\n", " ", unidecode(verse.text.strip()))
            if lyrics == "":
                lyrics = lyrics + lines.replace("\n","$")
            else:
                lyrics = lyrics + '$' + lines.replace("\n","$")
        allLyrics.append(lyrics)

    except urllib2.URLError as e:
        print e.reason


with open('lyricsData.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    for lyrics in allLyrics:
        writer.writerow([lyrics])


