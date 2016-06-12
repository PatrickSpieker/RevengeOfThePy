
class InvalidQueryException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Query:
    def __init__(self, *args):
        raise NotImplementedError('users must override init to use this class')

    def execute(self, *args):
        raise NotImplementedError('users must override execute to use this class')

    def __str__(self):
        return self.query


class Select(Query):
    def __init__(self, table_name, col_names=None):
        query = "SELECT "
        if not col_names:
            query += "*"
        else:
            for col in col_names[:len(col_names)-1]:
                query += col + ","
            query += col_names[len(col_names)-1]
        query += " FROM " + table_name
        self.query = query

    def execute(self, cur):
        cur.execute(self.query)


class Update(Query):
    def __init__(self, table_name, col_to_val, filter_col_val=None):
        query = "UPDATE " + table_name + " SET "
        
        for pair in col_to_val[:len(col_to_val)-1]:
            query += pair[0] + "=" + pair[1] + ","
        
        last = col_to_val[len(col_to_val)-1]
        query += last[0] + "=" + last[1]

        if filter_col_val:
            query += " WHERE " + filter_col_val[0] + "=" + filter_col_val[1] + ";"

        self.query = query

    def execute(self, cur):
        cur.execute(self.query)


class Delete(Query):
    def __init__(self, table_name, filter_col=None, filter_val=None):
        query = "DELETE FROM " + table_name

        if filter_col and filter_val:
            if not filter_val:
                raise InvalidQueryException()
            query += " WHERE " + filter_col
            if filter_val == "NULL":
                query += " IS NULL"
            else:
                query += "=" + filter_val

        query += ";"

        self.query = query

    def execute(self, cur):
        cur.execute(self.query)


class InsertInto(Query):
    def __init__(self, table_name, vals, cols=None):
        if cols and (len(cols) != len(vals)):
            raise InvalidQueryException()

        # generating the query from object's state
        query = "INSERT INTO " + table_name + " "
        
        if cols:
            query += "("
            for col in cols[:len(cols)-1]:
                query += col + ", "
            query += cols[len(cols)-1] + ") "  # manually adding the last one
        
        query += "VALUES ("
        for val in vals[:len(vals)-1]:
            query += "\'" + val + "\'" + ", "
        query += "\'" + vals[len(cols)-1] + "\'"
        query += ");"

        self.query = query

    def execute(self, cur):
        cur.execute(self.query)








