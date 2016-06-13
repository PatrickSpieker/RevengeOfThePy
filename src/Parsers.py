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
        if self.is_empty():
            raise StopIteration
        else:
            return self.reader.next()

    def is_empty(self):
        if next(self.reader, None):
            return False
        else: 
            return True
