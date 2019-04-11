from rq import Queue
from redis import Redis
import mysql.connector
from datetime import datetime

def removeUnconfirmedReservations():
 db = mysql.connector.connect(user='django', password='virurohan', 
                                database='bookmyslot')
 cursor=db.cursor()
 currtime=datetime.datetime.now() - datetime.timedelta(minutes=10)
 currtime=currtime.strftime('%Y-%m-%d %H:%M:%S')
 q="""SELECT ReservationID  FROM Reservation WHERE BookingTime < %s AND ReservationStatus = %s ;"""
 d=(currtime, 0)
 cursor.execute(q, d)

 result=cursor.fetchall()
 print("result: ", result)


# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue(connection=redis_conn)  # no args implies the default queue

# Delay execution of count_words_at_url('http://nvie.com')
job = q.enqueue(removeUnconfirmedReservations)
print(job.result)   # => None

# Now, wait a while, until the worker is finished
time.sleep(2)
print(job.result