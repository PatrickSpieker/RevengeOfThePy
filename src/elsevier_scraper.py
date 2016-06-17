import csv
from datetime import date

with open("../data/elsevier/2016-uncleaned-csv.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    with open("../data/cleaned/elsevier.csv", "w") as g:
        writer = csv.writer(g)
        writer.writerow(["pub_name", "journal_name", "date", "journal_type", "issn", "apc"])
        for row in reader:
            if row[0] == "Elsevier OA Price List":
                next(reader)
                next(reader)
            else:
                row[1] = " ".join(row[1].replace("\xa0", "").replace("\xd0", "")
                                        .replace("fee not payable by author", "")
                                        .replace("\x97", "").replace("\x83", "")
                                        .strip().split("\xca"))
                row = ["Elsevier", row[1], str(date.today()), 'Hybrid' if row[2] == 'Hybrid' else 'OA',
                       row[0], row[4]]
                print row
                writer.writerow(row)
