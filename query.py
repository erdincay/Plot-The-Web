import random
import os
import subprocess
import traceback
import time
from geoip import geolite2
import csv
from multiprocessing.pool import ThreadPool, Pool


null = open(os.devnull, 'w')

w,x,y,z=0,0,0,0

def get_ip():
    global w,x,y,z
    if z != 255:
        z+=1
    elif y != 255:
        y+=1
    elif x != 255:
        x+=1
    elif w != 255:
        w+=1
    else:
        return None
    return '.'.join(map(str,( i for i in (w,x,y,z))))



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
    pinged = []

    def cb(result):
        if result is None:
            return
        ip, lat, lon, t = result

    for i in range(10000):
        ip = get_random_ip()
        pinged.append(ip)
        match = geolite2.lookup(ip)
        if match is None or match.location is None:
            continue
        lat,lng = match.location
        pool.apply_async(ping,args=(ip,lat,lng),callback=cb)

    pool.close()
    pool.join()

    f.close()
