from __future__ import absolute_import, unicode_literals
from celery import task
import mysql.connector
import datetime

BOOKING_TIMEOUT = 5
TIMEZONE = 5.5
CONFIDENCE = 3
SCANNING_TIMEOUT = 5

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
 curr_time=datetime.datetime.now()  + datetime.timedelta(hours = TIMEZONE) - datetime.timedelta(minutes=BOOKING_TIMEOUT)
 cursor = db.cursor()
 q = "UPDATE Slots SET ReservationID = %s, EndTime = %s WHERE occupied = %s AND CNNFlag = %s AND ReservationID IS NOT NULL AND confidence > %s"
 d = (None, None, 0, 0, CONFIDENCE)
 cursor.execute(q, d)
 count = cursor.rowcount
 db.commit()
 cursor.close()
 db.close()
 return count

@task()
def detect_not_exiting():
 db = mysql.connector.connect(user='django', password='virurohan', 
                                database='bookmyslot')
 curr_time=datetime.datetime.now()  + datetime.timedelta(hours = TIMEZONE)
 cursor = db.cursor()
 q = "SELECT SlotID, ReservationID, EndTime FROM Slots WHERE occupied = %s AND ReservationID IS NOT NULL AND EndTime < %s AND confidence > %s"
 d =(1,curr_time, CONFIDENCE)
 cursor.execute(q, d)
 result = cursor.fetchall()
 count = cursor.rowcount
 if count > 0:
  for i in result:
   q = "INSERT INTO PenaltyReservations (ReservationID, SlotID, EndTime, LastSeenTime) VALUES(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE LastSeenTime=%s"
   d = (i[1], i[0], i[2], curr_time, curr_time) 
   cursor.execute(q,d)     
 db.commit()
 cursor.close()
 db.close()
 return count, curr_time

@task()
def detect_unauthorized_parkings():
 db = mysql.connector.connect(user='django', password='virurohan', 
                               database='bookmyslot')
 curr_time=datetime.datetime.now()  + datetime.timedelta(hours = TIMEZONE)
 cursor = db.cursor()
 q = "SELECT SlotID, CNNTimestamp FROM Slots WHERE occupied = %s AND CNNFlag = %s AND confidence > %s AND CNNTimestamp < %s"
 d =(1,1, CONFIDENCE, curr_time)
 cursor.execute(q, d)
 result = cursor.fetchall()
 count = cursor.rowcount
 if count > 0:
  for i in result:
   q = "INSERT INTO UnauthorizedParkings (SlotID, StartTime, LastSeenTime) VALUES(%s, %s, %s) ON DUPLICATE KEY UPDATE LastSeenTime=%s"
   d = (i[0], i[1],curr_time, curr_time) 
   cursor.execute(q,d)     
 db.commit()
 cursor.close()
 db.close()
 return count, curr_time
