import pandas as pd

# Load your cleaned dataset
file_path = 'equigen_dataset.tsv'
data = pd.read_csv(file_path, sep='\t')

# Counting the number of albums per genre
albums_per_genre = data['genre'].value_counts()

# Displaying the number of albums per genre
print(albums_per_genre)
