import threading
import random
import time, sqlite3

class myThread(threading.Thread):

   def __init__(self, param):
       threading.Thread.__init__(self)
       self.param = param

   def run(self):
       con = sqlite3.connect("DB.db", check_same_thread=False)
       cursor = con.cursor()
       cursor.execute("create table if not exists people(name text, value real)")
       cursor.execute(self.param)
       con.commit()
       con.close()

while True:
    names = ['Ania', 'Natasha', 'Guido van Rossum', 'Kate', 'Papa John']
    threadpool = []
    for i in range(10):
        name = random.choice(names)
        value = random.randrange(0, 10)
        result = "insert into people values({}, {})".format('"' + name + '"', value)
        threadpool.append(myThread(result))
        result = "delete from people where value = 4 or value = 0"
        threadpool.append(myThread(result))
    for t in threadpool:
        t.start()
    for t in threadpool:
        t.join()
