import random
import os
import subprocess
import traceback
import time
from geoip import geolite2
import csv
from multiprocessing.pool import ThreadPool, Pool


null = open(os.devnull, 'w')


def get_random_ip():
    return '.'.join(map(str, [random.randint(0, 255) for i in xrange(4)]))


def ping(ip,lat,lng):
    try:
        t = time.time()
        status = subprocess.call(['ping', '-c2', ip], stdout=null, stderr=null)
        if status != 0:
            return None
        return ip,lat,lng,time.time() - t
    except:
        traceback.print_exec()

if __name__ == '__main__':
    pool = ThreadPool(processes=100)
    f = open('data','w')

    def cb(result):
        if result is None:
            return
        print
        print result
        print
        ip, lat, lon, t = result
        (f.write(x+"\n") for x in result)

    for i in range(100):
        ip = get_random_ip()
        match = geolite2.lookup(ip)
        if match is None or match.location is None:
            continue
        lat,lng = match.location
        pool.apply_async(ping,args=(ip,lat,lng),callback=cb)

    pool.close()
    pool.join()

    f.close()
