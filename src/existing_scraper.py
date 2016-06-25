import csv
from datetime import date
with open("../data/OA_journals.tsv", "rU") as f:
    reader = csv.reader(f, dialect=csv.excel_tab)
    next(reader)
    with open("../data/cleaned/original_converted.csv", "w") as g:
        writer = csv.writer(g)
        writer.writerow(["pub_name", "journal_name", "date", "journal_type", "issn", "apc"])
        for row in reader:
            #print row
            if row[2]:
                row = [row[0], row[1], str(date.today()), "OA" if row[7] else "Hybrid", row[2], row[6]]
                print row
                writer.writerow(row)


