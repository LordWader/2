from threading import Thread
import random
from queue import Queue
import sqlite3
 
class SQL_db(Thread):
    """
    part of code is under MIT License
    FAQ:
    why sqlite3 - Because we have only one connection. For many connections is better to use sqlalchemy, mysql or whatever you want
    wtf is Queue - Thats special. If you know how to implement multithreading programm with safely exchanged
    information between threads and also know locking semantics - give it a try. You dont't need to check if the thread
    is available or not. Just use queue and everything will be ok.
    """
    def __init__(self, db):
        super().__init__()
        self.db=db
        self.reqs=Queue() 
        self.start()
        
    def run(self):
        cnx = sqlite3.Connection(self.db) 
        cursor = cnx.cursor()
        while True:
            req, arg, res = self.reqs.get()
            if req=='--close--':
                break
            cursor.execute(req, arg)
            if res:
                for rec in cursor:
                    res.put(rec)
                    cnx.commit()
                res.put('--no more--')
        cnx.close()
        
    def execute(self, req, arg=None, res=None):
        self.reqs.put((req, arg or tuple(), res))
        
    def select(self, req, arg=None):
        res=Queue()
        self.execute(req, arg, res)
        while True:
            rec=res.get()
            if rec=='--no more--':
                break
            yield rec
 
    def delete(self, req, arg = None):
        res=Queue()
        return self.execute(req, arg, res)
 
    def update(self, req, arg = None):
        res=Queue()
        return self.execute(req, arg, res)

            
    def close(self):
        self.execute('--close--')
 
if __name__=='__main__':
 
    db='people.db'
    sql = SQL_db(db)
    names = ['Ania', 'Natasha', 'Guido van Rossum', 'Kate', 'Papa John']
    sql.execute("create table if not exists people(name text, value real)")
    for i in range(5):
        name = random.choice(names)
        value = random.randrange(0, 10)
        sql.execute("insert into people values(?, ?)", (name, value))
    sql.delete("delete from people where value = 4")
    sql.update("update people set name = 'Kate' where name = 'Papa John'")
    for f, n in sql.select("select name, value from people where value = 1"):
        print (f, n)
    sql.close()
