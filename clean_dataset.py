import csv
import re

# Define the path for the original TSV file (which will be modified in place)
tsv_path = 'equigen_dataset.tsv'

# Regular expression to match asterisks and numbers in parentheses
pattern = re.compile(r'\*|\(\d+\)')

# Read from the original TSV into memory
with open(tsv_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter='\t')
    # Convert the reader to a list to store all rows in memory
    rows = list(reader)
    fieldnames = reader.fieldnames

# Modify the data in memory
for row in rows:
    # Remove asterisks and numbers in parentheses from the artist name
    row['artist'] = re.sub(pattern, '', row['artist']).strip()

# Write the modified data back to the same TSV file
with open(tsv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    writer.writerows(rows)

print("Finished processing the TSV file in place.")
