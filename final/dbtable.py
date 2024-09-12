# Базовые действия с таблицами

from dbconnection import *

'''
FIXME:
'''

class DbTable:
    dbconn = None

    def __init__(self):
        return

    def table_name(self):
        return self.dbconn.prefix + "table"

    def columns(self):
        return {"test": ["integer", "PRIMARY KEY"]}

    def column_names(self):
        return sorted(self.columns().keys(), key = lambda x: x)

    def primary_key(self):
        return ['id']

    def column_names_without_id(self):
        res = sorted(self.columns().keys(), key = lambda x: x)
        if 'id' in res:
            res.remove('id')
        return res

    def table_constraints(self):
        return []

    def create(self):
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in sorted(self.columns().items(), key = lambda x: x[0])]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def drop(self):
        sql = "DROP TABLE IF EXISTS " + self.table_name()
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def insert_one(self, vals):
        for i in range(len(vals)):
            if type(vals[i]) == str:
                vals[i] = "'" + vals[i] + "'"
            else:
                vals[i] = str(vals[i])
        values = ", ".join(vals)
        query = f"""INSERT INTO {self.table_name()}({", ".join(self.column_names_without_id())}) VALUES({values})"""
        cur = self.dbconn.conn.cursor()
        # cur.execute(sql)
        try:
            cur.execute(query)
            self.dbconn.conn.commit()
        except psycopg2.errors.UniqueViolation:
            self.dbconn.conn.rollback()
            print('Такая строка уже существует. Повторите попытку')
        return

    def update(self, column, values, wh):
        sql = f"UPDATE {self.table_name()} SET {column} = {values} WHERE id = {wh};"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def first(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()        

    def last(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join([x + " DESC" for x in self.primary_key()])
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def all(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()        
        
    def select_one(self, **kwargs):
        conditions = []
        values = []
        
        sorted_kwargs = sorted(kwargs.items(), key=lambda x: x[0])
        
        for key, value in sorted_kwargs():
            conditions.append(f"{key}=%s")
            values.append(value)

        sql = f"SELECT * FROM {self.table_name()} WHERE " + " AND ".join(conditions)
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, tuple(values))
        result = cur.fetchone()
        cur.close()

        if result:
            return True
        else:
            return False
        


