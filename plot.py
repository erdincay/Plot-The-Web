import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from annoy import AnnoyIndex
from mpl_toolkits.basemap import Basemap
import json




def convert(lat, lon):
    lat *= math.pi / 180
    lon *= math.pi / 180
    x = math.cos(lat) * math.cos(lon)
    z = math.cos(lat) * math.sin(lon)
    y = math.sin(lat)
    return [x, y, z]


def main():

    ai = AnnoyIndex(3, 'angular')
    xs, ys, ts = [], [], []
    cords = {}
    data = json.load(open('data.json'))

    for x in data:

        ip,lat,lon,t = x[0],x[1],x[2],x[3]
        cords.setdefault((lat, lon), []).append(t)

    for c,t in cords.iteritems():

        lat, lon = c
        t = np.median(t)
        p = convert(lat, lon)
        ai.add_item(len(ts), p)
        xs.append(lon)
        ys.append(lat)
        ts.append(t)

    ai.build(10)
    print ai
    lons = np.arange(-180, 180, 0.25)
    lats = np.arange(-90, 90, 0.25)
    X, Y = np.meshgrid(lons, lats)
    Z = np.zeros(X.shape)
    count = 0
    for i, _ in np.ndenumerate(Z):
        lon, lat = X[i], Y[i]

        v = convert(lat, lon)

        js = ai.get_nns_by_vector(v, 50)
        #print js
        all_ts = [ts[j] for j in js]
        #print all_ts


if __name__ == '__main__':
    main()
