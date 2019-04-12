
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import os
import time
import mysql.connector
import datetime
def addTwo():
 db = mysql.connector.connect(user='django', password='virurohan', 
                                database='bookmyslot')
 curr_time=datetime.datetime.now() - datetime.timedelta(minutes=10)
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
  return False