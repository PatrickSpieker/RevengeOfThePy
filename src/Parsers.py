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

    def readline(self):
        if self.isEmpty():
            raise StopIteration
        else:
            return self.reader.next()

    def isEmpty(self):
        if next(self.reader, None):
            return False
        else: 
            return True
    
class OAJournalParser(TSVParser):
    def __init__(self, file_name):
        super(OAJournalParser, self).__init__(file_name)


