from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import redis
import mysql.connector
from datetime import datetime
import os
import time

from addTwo import *
from rq import Connection, Queue


def main():
    # Range of Fibonacci numbers to compute
    #fib_range = range(20, 34)

    # Kick off the tasks asynchronously
    async_results = {}
    q = Queue()
    start_time = time.time()
    done = False
    x = 0
    while not done:
        os.system('clear')
        print('Asynchronously: (now = %.2f)' % (time.time() - start_time,))
        #done = True
        async_results[x] = q.enqueue(addTwo)
        x += 1
        print('')
        print('To start the actual in the background, run a worker:')
        print('    python qworker.py')
        time.sleep(60*10)

    print('Done')


if __name__ == '__main__':
    # Tell RQ what Redis connection to use
    with Connection():
    	main()