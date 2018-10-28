import threading
import random
import sqlite3

class SQL_db:
    def __init__(self, db):
        self.db = db
        self.conn = None
        self.lock = threading.Lock()

        with self.lock:
            with self.connect() as conn:
                conn.execute('create table if not exists people(name text, value real)')

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db, check_same_thread = False)
        return self.conn
        
    def select(self, key = None, value = None):
        with self.lock:
            cursor = self.connect().cursor()
            if key == None and value == None:
                cursor.execute('select * from people')
            else:
                cursor.execute('select %s from people where value = ?' % key, (value,))

    def insert(self, name = None, value = None):
        with self.lock:
            with self.connect() as conn:
                conn.execute('insert or replace into people values(?, ?)', (name, value) )
        

    def delete(self, key = None):
        with self.lock:
            with self.connect() as conn:
                if type(key) == str:
                    conn.execute('delete from people where name = ?', (key,))
                else:
                    conn.execute('delete from people where value = ?', (key,))

    def update(self, prev, fut):
        with self.lock:
            with self.connect() as conn:
                if type(prev) == str:
                    conn.execute('update people set name = ? where name = ?',(fut, prev))
                else:
                    conn.execute('update people set value = ? where value = ?', (fut, prev))
            

if __name__=='__main__':

    db = 'people.db'
    sql = SQL_db(db)
    names = ['Ania', 'Natasha', 'Guido van Rossum', 'Nick Proshin', 'Papa John']
    for i in range(20):
        name = random.choice(names)
        value = random.randrange(0, 10)
        sql.insert(name, value)
    sql.delete('Papa John')
    sql.update('Ania', 'Nickita')
    sql.update(8, 100)
