import random
import os
import subprocess
import traceback
import time
from geoip import geolite2
import csv
from multiprocessing.pool import ThreadPool, Pool
import json
import itertools

null = open(os.devnull, 'w')


def get_random_ip():
    return '.'.join(map(str, [random.randint(0, 255) for i in xrange(4)]))


def ping(ip,lat,lng):
    try:
        t = time.time()
        status = subprocess.call(['ping', '-c4  ', ip], stdout=null, stderr=null)
        if status != 0:
            return None
        return ip,lat,lng,time.time() - t
    except:
        traceback.print_exec()

if __name__ == '__main__':
    pool = ThreadPool(processes=100)
    outfile= open('data2.json', 'a')
    res = []
    def cb(result):
        if result is None:
            return
        print result
        ip, lat, lon, t = result
        res.append((ip,lat,lon,t))

    for i in itertools.count(429496729):
        ip = get_random_ip()
        match = geolite2.lookup(ip)
        if match is None or match.location is None:
            continue
        lat,lng = match.location
        pool.apply_async(ping,args=(ip,lat,lng),callback=cb)

    pool.close()
    pool.join()
    json.dump(res, outfile,indent = 4)

    outfile.close()
