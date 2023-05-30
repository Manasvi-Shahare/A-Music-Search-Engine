#api token for genius.com website
GENIUS_API_TOKEN='ZQEoc3jPsYWwnW-Aqa1_5GsaVKyre20WzVIVTFACQzp08gDUcSVSzzA78do7h7f5'

import collections.abc
from collections.abc import Mapping
collections.Callable = collections.abc.Callable

# Make HTTP requests
import requests
# Scrape data from an HTML document
from bs4 import BeautifulSoup
# I/O
import os
# Search and manipulate strings
import re
#to store the scraped data in json format
import json

#an array for storing the scraped object
a = []
# Function to make a request to the Genius API and get artist info
def request_artist_info(artist_name, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    if response.status_code == 200:
        return response
    else:
        raise Exception('Request failed with status code', response.status_code)

# Function to get song URLs from artist object
def request_song_url(artist_name, song_cap):
    page = 1
    songs = []
    while True:
        response = request_artist_info(artist_name, page)
        json = response.json()
        song_info = []
        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_info.append(hit)
        for song in song_info:
            if (len(songs) < song_cap):
                url = song['result']['url']
                songs.append(url)
                print(url)
        if (len(songs) == song_cap):
            break
        else:
            page += 1
    print('Found {} songs by {}'.format(len(songs), artist_name))
    return songs

# Function to scrape lyrics from a Genius.com song URL
def scrape_song_lyrics(url):
    page = requests.get(url)
    if page.status_code != 200:
        raise Exception('Failed to retrieve page', url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics_container = html.find('div', class_='Lyrics__Container-sc-1ynbvzw-6 YYrds')
    if lyrics_container:
        lyrics = lyrics_container.get_text()
        title = html.find('title').text.strip().replace(' Lyrics | Genius Lyrics', '')
        artist = artist_name
        # Remove identifiers like chorus, verse, etc
        lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
        # Remove empty lines
        lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
        if lyrics:
            obj = {
                'artist': artist,
                'title': title,
                'lyrics': lyrics,
                'url': url
            }
            a.append(obj)
            closed(a)
            print(a)
            return [[lyrics]]
        else:
            raise Exception('No lyrics found for', url)
    else:
        raise Exception('No lyrics container found for', url)

# Function to store scraped data in a JSON file
def closed(new_data, filename='scraped_songs.json'):
    with open(filename, 'w', encoding="utf8") as outfile:
        json.dump(new_data, outfile, indent=4, ensure_ascii=False)

#write scraped song lyrics to a json file
def write_lyrics_to_file(artist_name, song_count):
    response = request_artist_info(artist_name, 1)
    urls = request_song_url(artist_name, song_count)
    for url in urls:
        try:
            lyrics = scrape_song_lyrics(url)
        except Exception as e:
            print(f"Error scraping lyrics for song at URL {url}: {e}")
            continue

    print('Done')

    #print('Wrote {} lines to file from {} songs'.format(num_lines, song_count))

# Read in artist names from file
with open('artists.txt') as f:
    artist_names = [line.strip() for line in f.readlines()]

# Loop through artist names and scrape lyrics
for artist_name in artist_names:
    print(f"Scraping lyrics for {artist_name}")
    write_lyrics_to_file(artist_name, 100)
