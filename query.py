import random
import os
import subprocess
import traceback
import time
from multiprocessing.pool import ThreadPool, Pool


null = open(os.devnull, 'w')


def get_random_ip():
    return '.'.join(map(str, [random.randint(0, 255) for i in xrange(4)]))


def ping(ip,lat,lng):
    try:
        print ip
        t = time.time()
        status = subprocess.call(['ping', '-c1', '-t2', ip], stdout=null, stderr=null)
        if status != 0:
            return None
        return ip,lat,lng,time.time() - t
    except:
        traceback.print_exec()

if __name__ == '__main__':
    pool = ThreadPool(processes=100)
    f = open('data','a')
