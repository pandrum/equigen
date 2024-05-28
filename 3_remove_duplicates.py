import pandas as pd

# Load the dataset
# Make sure to replace this with the path to your dataset
file_path = 'equigen_dataset.tsv'
data = pd.read_csv(file_path, sep='\t')

# Create a unique identifier for artist-album combinations
data['artist_album'] = data['artist'] + " - " + data['album']

# Drop duplicates based on the artist-album combination
data_unique_artist_album = data.drop_duplicates(
    subset='artist_album', keep='first')

# Drop duplicates based on the image URL
data_final = data_unique_artist_album.drop_duplicates(
    subset='image_url', keep='first')

# Save the cleaned dataset back to the original file
data_final.to_csv(file_path, sep='\t', index=False)

print(f"Cleaned dataset saved back to {file_path}")
