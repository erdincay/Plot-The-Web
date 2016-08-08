import math
import numpy
from annoy import AnnoyIndex
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from mpl_toolkits import basemap

vmin, vmax = 0.0, 0.4

def convert(lat, lon):


def ll_to_3d(lat, lon):
    lat *= math.pi / 180
    lon *= math.pi / 180
    x = math.cos(lat) * math.cos(lon)
    z = math.cos(lat) * math.sin(lon)
    y = math.sin(lat)
    return [x, y, z]

cords = {}
for line in open('data'):
    try:
        lat, lon, t = map(float, line.strip().split())
    except:
        print 'could not parse',line
        continue
    cords.setdefault((lat,lng),[]).append(t)

ai = AnnoyIndex(3, 'angular')
xs, ys, ts = [], [], []

for c, ip in coords.iteritems():
    lat, lon = c
    ip = np.median(ip) # remove duplicate ips with same lat/long
    p = convert(lat, lon)
    ai.add_item(len(ts), p)
    xs.append(lon)
    ys.append(lat)
    ts.append(t)


ai.build()

lons = np.arange(-180, 180, 0.25)
lats = np.arange(-90, 90, 0.25)
x,y = np.meshgrid(lons,lats)
z = np.zeros(x.shape)
for i, _ in np.ndenumerate(Z):
    lon, lat = x[i], y[i]
    v = convert(lat,lon)
    js = ai.get_nns_by_vector(v, 50)
    all_ts = [ts[j] for j in js]
