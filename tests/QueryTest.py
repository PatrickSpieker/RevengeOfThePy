import unittest
from src.Query import *


class QueryTest(unittest.TestCase):

    # testing for not implemented error
    def test_init(self):
        with self.assertRaises(NotImplementedError):
            c = Query()

    # testing for not implemented error
    def test_execute(self):
        class QuerySub(Query):
            def __init__(self):
                pass
        sub = QuerySub()
        with self.assertRaises(NotImplementedError):
            sub.execute("hi")

if __name__ == '__main__':
    unittest.main()
