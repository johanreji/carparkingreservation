from __future__ import absolute_import, unicode_literals
from celery import task
import mysql.connector
import datetime

BOOKING_TIMEOUT = 5
TIMEZONE = 5.5

@task()
def booktimer():
 db = mysql.connector.connect(user='django', password='virurohan', 
                                database='bookmyslot')
 curr_time=datetime.datetime.now()  + datetime.timedelta(hours = TIMEZONE) - datetime.timedelta(minutes=BOOKING_TIMEOUT)
 print(curr_time)
 cursor = db.cursor()
 q = "SELECT ReservationID FROM Reservation WHERE BookingTime < %s AND ReservationStatus = %s"
 d=(curr_time, 0)
 cursor.execute(q,d)
 result=cursor.fetchall()
 num_count=cursor.rowcount
 if(num_count>0):
  result_list = list(map(lambda x: x[0], result)) 
  print(result_list)
  format_strings = ','.join(['%s'] * len(result_list))
  cursor.execute("DELETE FROM ReservedSlots WHERE ReservationID IN (%s)" % format_strings,
                tuple(result_list))
  cursor.execute("DELETE FROM Reservation WHERE ReservationID IN (%s)" % format_strings,
                tuple(result_list))
 
  db.commit()
  cursor.close()
  db.close()
  return True
 else:
  return False, curr_time

@task()
def detect_exit():
 db = mysql.connector.connect(user='django', password='virurohan', 
                                database='bookmyslot')
 #curr_time=datetime.datetime.now()  + datetime.timedelta(hours = TIMEZONE) - datetime.timedelta(minutes=BOOKING_TIMEOUT)
 cursor = db.cursor()
 q = "SELECT"
 q = "UPDATE Slots SET ReservationID = %s, EndTime = %s WHERE occupied = %s AND CNNFlag = %s AND ReservationID IS NOT NULL"
 d = (None, None, 0, 0)
 cursor.execute(q, d)
 count = cursor.rowcount
 db.commit()
 cursor.close()
 db.close()
 return count
