import csv
from datetime import date
with open("../data/cleaned/springer.csv", "a") as f:
    writer = csv.writer(f)

    with open("../data/springer/2016+Springer+Journals+List.csv") as g:
        reader = csv.reader(g)
        for i in range(9):
            next(reader)
        for i in reader:
            if i[11] == "Hybrid (Open Choice)":
                row = ["Springer", i[1], str(date.today()), "Hybrid", i[5], 3000]
                print row
                writer.writerow(row)
