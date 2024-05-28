from datetime import datetime
from time import sleep
import requests
import csv
import os


# API credentials
api_key = 'svZecStgWNJNxVCdXadr'
api_secret = 'cpJxYMiWPnHWOOXnsDeppfTBiBmwWmLR'

# Updated list of genres, styles, and world music subgenres
genres_styles = {
    'Blues': 'genre',
    'Country': 'genre',
    'Electronic': 'genre',
    'Jazz': 'genre',
    'Latin': 'genre',
    'Reggae': 'genre',
    'Pop': 'genre',
    'Rock': 'genre',
    'Folk': 'style',
    'Metal': 'style',
    'New Age': 'style',
    'Punk': 'style',
    'Rap': 'style',
    'Rhythm & Blues': 'style',
}

world_subgenres = {
    'Afrobeat': 'style',
    'Rumba': 'style',
    'Celtic': 'style',
    'Flamenco': 'style',
    'Bollywood': 'style',
    'Hindustani': 'style',
    'K-Pop': 'style',
    'Mandopop': 'style',
    'Salsa': 'style',
    'Bolero': 'style'
}

# Placeholder image URL and headers
placeholder_substring = 'spacer.gif'
headers = {
    'User-Agent': 'music-dataset/1.0 +https://github.com/pandrum/music-dataset',
    'Authorization': f'Discogs key={api_key}, secret={api_secret}'
}

# CSV file setup
script_dir = os.path.dirname(os.path.realpath(__file__))
tsv_file_path = os.path.join(script_dir, 'equigen_dataset.tsv')

# Initialize unique entry tracking, unique image URL tracking, and unique artist-genre tracking
genre_limit = 15000  # Limit for each genre
world_limit = 1200  # Limit per world subgenre

unique_entries = set()
unique_image_urls = set()
unique_artist_genre = {}  # Using dict to track artist-genre combination uniquely
row_counts = {**{genre: 0 for genre in genres_styles},
              **{subgenre: 0 for subgenre in world_subgenres}}

# Load existing data to prevent duplicates
if os.path.isfile(tsv_file_path) and os.path.getsize(tsv_file_path) > 0:
    with open(tsv_file_path, mode='r', newline='', encoding='utf-8') as tsv_file:
        reader = csv.DictReader(tsv_file, delimiter='\t')
        for row in reader:
            unique_entries.add(f"{row['artist']}|{row['album']}")
            unique_image_urls.add(row['image_url'])
            # Ensure we track artist-genre combination correctly
            unique_artist_genre[row['artist']] = row['genre']


def make_request_with_backoff(url):
    backoff_time = 1  # Initial backoff time
    max_attempts = 10
    attempt = 0

    while attempt < max_attempts:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if e.response.status_code in [429, 500]:
                print(f"{e.response.reason}, retrying...")
            elif e.response.status_code == 404:
                print("Record not found, skipping...")
                return None  # Skip this entry
            elif e.response.status_code == 502:
                print(
                    f"Bad Gateway (HTTP 502) encountered for URL: {url}. Skipping this entry.")
                return None  # Skip this entry
            else:
                print(f"HTTP error occurred: {e} - {e.response.status_code}")

            sleep(backoff_time)
            backoff_time *= 2
            attempt += 1
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    raise Exception("Maximum retry attempts reached, aborting.")


def adjust_search_url(genre, search_param, year):
    base_url = f"https://api.discogs.com/database/search?format=album&per_page=100&year={year}"
    if genre in ['Blues', 'Country', 'Jazz', 'Pop', 'Rock']:
        base_url += f"&genre={genre}&style={genre}"
    else:
        base_url += f"&{search_param}={genre}"
    return base_url


def should_fetch_genre(genre):
    if genre in world_subgenres and row_counts[genre] >= world_limit:
        return False
    elif genre in genres_styles and row_counts[genre] >= genre_limit:
        return False
    return True


mode = 'a' if os.path.isfile(tsv_file_path) and os.path.getsize(
    tsv_file_path) > 0 else 'w'
with open(tsv_file_path, mode=mode, newline='', encoding='utf-8') as tsv_file:
    fieldnames = ['artist', 'album', 'album_index',
                  'genre', 'year', 'image_url']
    writer = csv.DictWriter(tsv_file, fieldnames=fieldnames, delimiter='\t')
    if mode == 'w':
        writer.writeheader()

    for genre, type_or_tag in {**genres_styles, **world_subgenres}.items():
        year = datetime.now().year
        while should_fetch_genre(genre):
            print(f"Fetching albums for {genre} for the year {year}...")
            search_param = 'style' if type_or_tag == 'style' else 'genre'
            base_url = adjust_search_url(genre, search_param, year)

            response = make_request_with_backoff(base_url)
            if not response:  # Skip this genre/year combination if the request failed
                break

            data = response.json()
            total_pages = data['pagination']['pages']
            for page in range(1, total_pages + 1):
                print(f"Fetching page {page} for {genre} in the year {year}.")
                page_url = f"{base_url}&page={page}"
                page_response = make_request_with_backoff(page_url)
                if not page_response:  # Skip this page if the request failed
                    continue

                page_data = page_response.json()
                for item in page_data['results']:

                    # Skip items with 'Cassette' in their formats
                    if any(format['name'] == 'Cassette' for format in item.get('formats', []) if 'name' in format):
                        continue

                        # New check to skip Rhythm & Blues when fetching Blues
                    if genre == 'Blues' and 'Rhythm & Blues' in item.get('style', []):
                        continue  # Skip this album as it includes Rhythm & Blues style

                    title = item.get('title', '')
                    artist_name, album_name = title.split(
                        ' - ', 1) if ' - ' in title else (title, '')
                    image_url = item.get('cover_image', '')
                    unique_id = f"{artist_name}|{album_name}"

                    # Ensure we respect genre exclusivity per artist
                    if artist_name in unique_artist_genre:
                        if unique_artist_genre[artist_name] != genre:
                            continue
                    else:
                        unique_artist_genre[artist_name] = genre

                    # Skip entries with placeholder images or duplicates
                    if placeholder_substring in image_url or unique_id in unique_entries or image_url in unique_image_urls:
                        continue

                    # Check if the genre is in the world_subgenres dictionary
                    genre_label = genre
                    if genre in world_subgenres:
                        # Append "(World)" to the genre label
                        genre_label += " (World)"

                    writer.writerow({
                        'artist': artist_name,
                        'album': album_name,
                        'album_index': row_counts[genre] + 1,
                        'genre': genre_label,  # Use the modified genre label here
                        'year': item.get('year', year),
                        'image_url': image_url
                    })
                    unique_entries.add(unique_id)
                    unique_image_urls.add(image_url)
                    row_counts[genre] += 1

                if not should_fetch_genre(genre):
                    break
                sleep(1)

            year -= 1
            if year < 1930 or not should_fetch_genre(genre):
                break

print(f"Dataset has been created at {tsv_file_path}.")
