import csv
import os
import requests
from requests.exceptions import HTTPError
from time import sleep

# API credentials
api_key = 'svZecStgWNJNxVCdXadr'
api_secret = 'cpJxYMiWPnHWOOXnsDeppfTBiBmwWmLR'

# Update the file path for the TSV file
# Update to the correct path where the TSV file is saved
tsv_file_path = 'equigen_dataset.tsv'
images_folder = 'equigen_album_images'

# Headers for the requests with User-Agent and Authorization
headers = {
    'User-Agent': 'music-dataset/1.0 +https://github.com/pandrum/music-dataset',
    'Authorization': f'Discogs key={api_key}, secret={api_secret}'
}

# Function to download an image from a URL


def download_image_with_backoff(image_url, filename):
    backoff_time = 1  # Start with 1 second
    max_attempts = 10
    attempt = 0

    while attempt < max_attempts:
        try:
            response = requests.get(image_url, headers=headers, stream=True)
            response.raise_for_status()

            with open(filename, 'wb') as out_file:
                for chunk in response.iter_content(chunk_size=8192):
                    out_file.write(chunk)
            print(f"Downloaded {filename}")
            break  # Success, exit the loop
        except HTTPError as e:
            if e.response.status_code == 429:  # Too many requests
                print(
                    f"Rate limited. Waiting {backoff_time} seconds before retrying...")
                sleep(backoff_time)
                backoff_time *= 2  # Double the wait time for the next attempt
                attempt += 1
            else:
                print(f"HTTP error occurred: {e} - {e.response.status_code}")
                break  # Exit loop for non-rate limit errors
        except Exception as e:
            print(f"An error occurred: {e}")
            break
        except KeyboardInterrupt:
            print("Download interrupted by user.")
            break


# Read the TSV and download images
with open(tsv_file_path, mode='r', newline='', encoding='utf-8') as tsv_file:
    reader = csv.DictReader(tsv_file, delimiter='\t')
    for row in reader:
        genre = row['genre']
        # Determine if genre should be categorized under 'World'
        if 'World' in genre:
            genre_folder = os.path.join(images_folder, 'World')
        else:
            # Place other genres in their respective folders
            genre_folder = os.path.join(images_folder, genre)

        # Create the genre subfolder if it doesn't exist
        os.makedirs(genre_folder, exist_ok=True)

        artwork_url = row['image_url']
        image_filename = f"{row['artist']} - {row['album']}.jpg".replace(
            '/', '_').replace(' ', '_')
        image_path = os.path.join(genre_folder, image_filename)

        # Skip download if image already exists
        if not os.path.exists(image_path):
            download_image_with_backoff(artwork_url, image_path)
            sleep(1.1)  # Sleep to avoid rate limiting
        else:
            print(
                f"Image {image_filename} already exists in genre folder {genre}.")

print("Finished downloading all images.")
