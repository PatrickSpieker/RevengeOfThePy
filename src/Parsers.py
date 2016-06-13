import csv
import sys


class TSVParser:
    def __init__(self, file_name):
        try:
            f = open(file_name)
        except IOError, e:
            print "The file \"" + file_name + "\" couldn't be opened"
            print e
            sys.exit(1)

        self.reader = csv.reader(f, dialect="excel-tab")

    def next(self):
        try:
            return self.reader.next()
        except StopIteration:
            raise StopIteration

    def __iter__(self):
        return self


class OAJournalsParser(TSVParser):
    def __init__(self, file_name):
        TSVParser.__init__(self, file_name)
        self.reader.next()

    @staticmethod
    def generate_pub_insert(row):
        return "INSERT INTO publishers VALUES ('" + row[0] + "','" + row[1] + "');"

    @staticmethod
    def _check_null(val):
        result = ""
        if (val == '') or (val == "NULL"):
            result += "NULL,"
        else:
            result += "'" + val + "',"
        return result

    @staticmethod
    def generate_journal_insert(row):
        journal_insert = "INSERT INTO journals VALUES ('" + row[1] + "',"
        journal_insert += OAJournalsParser._check_null(row[2])
        journal_insert += OAJournalsParser._check_null(row[3])
        journal_insert += row[4] + ","
        journal_insert += OAJournalsParser._check_null(row[5])
        journal_insert += row[6] + ","
        if row[7] == "1":
            journal_insert += "TRUE"
        else:
            journal_insert += "FALSE"
        journal_insert += ");"

        return journal_insert
