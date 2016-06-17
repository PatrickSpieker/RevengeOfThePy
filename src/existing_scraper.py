import csv
from datetime import date
with open("../data/OA_journals.tsv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    next(reader)
    with open("../data/cleaned/original_converted.csv", "w") as g:
        writer = csv.writer(g)
        for row in reader:
            row = [row[0], row[1], row[2]]


