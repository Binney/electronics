import csv

sounds = {}

with open("sounds-mapping.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sounds[row['Number']] = row

print(sounds)
