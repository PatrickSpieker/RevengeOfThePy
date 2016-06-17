import csv
paths_to_data = []

for path in paths_to_data:
    with open(path, 'r') as f:
        reader = csv.reader()
        next(reader)  # eliminating column names
        # do SQL stuff
