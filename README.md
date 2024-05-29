# EquiGen Album Cover Dataset
The "EquiGen Album Cover Dataset" repository contains a set of Python scripts for creating, cleaning, and processing a dataset of music album covers. 

The ```create_tsv.py``` script uses the Discogs API to fetch album data, ```clean_dataset.py``` and ```remove_duplicates.py``` clean the dataset, ```check_album_counts.py``` provides genre-wise album counts, ```download_equigen_images.py``` downloads album cover images, and ```split.py``` splits the images into training, validation, and test sets. 

These scripts enable the creation and preparation of a album cover dataset for machine learning.


### 1. create_tsv.py
This script uses the Discogs API to fetch data about music albums. It uses a list of genres and styles to fetch the data. The data is then written to a TSV file. 

To use the script, you need to create a Discog account and register a Discog application to have access to Discogs API endpoints. The ```api_key```, ```api_secret``` and ```User-Agent``` needs to be changed in the script to reflect your information. 

The ```genre_limit```and ```world_limit``` values can be changed to depending on how many entries you want for each of the major genres as well as the world subgenres when the TSV file is being populated.

The script handles rate limiting by the API by implementing a backoff strategy.

The output when executing the script is a TSV file named ```equigen_dataset.tsv``` with information about artist name, album name, index, genre, year and image_url for fetching the album cover. 

### 2. clean_dataset.py
This script reads the 'equigen_dataset.tsv' file into memory, removes asterisks and numbers in parentheses from the artist names, and writes the cleaned data back to the same file.

### 3. remove_duplicates.py
This script loads the 'equigen_dataset.tsv' file, removes any duplicate entries, and writes the cleaned dataset back to the same file.

### 4. check_album_counts.py
This script loads the cleaned 'equigen_dataset.tsv' file. It uses pandas to read the file and then counts the number of albums per genre in the dataset. The counts are then printed to the console.

### 5. download_equigen_images.py
This script downloads album cover images from the Discogs API. It reads the 'equigen_dataset.tsv' and downloads the images for each album. The script saves each album cover into a directory with the same name as the albums respective genre. The script handles rate limiting by the API by implementing a backoff strategy. The output results in the following structure:

```
equigen_album_images/
│
├── Blues/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
├── Country/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
├── Electronic/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
├── Folk/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
├── Jazz/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
├── Latin/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
├── Metal/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
├── New Age/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
├── Pop/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
├── Punk/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
├── Rap/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
├── Reggae/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
├── Rhythm & Blues/
│   ├── (album_cover_1).jpg
│   ├── (album_cover_2).jpg
│   └── ...
│
└── Rock/
    ├── (album_cover_1).jpg
    ├── (album_cover_2).jpg
    └── ...


```

### 6. split.py
This script uses the `split-folders` library to split the images in the 'equigen_album_images' folder into training, validation, and test sets. The split is done in a 70:15:15 ratio.

## Usage
To run the scripts in the correct order, use the following commands:
```bash
python create_tsv.py
python clean_dataset.py
python remove_duplicates.py
python check_album_counts.py
python download_equigen_images.py
python split.py
