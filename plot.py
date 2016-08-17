import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from mpl_toolkits import basemap
import json


def convert(lat, lon):
    lat *= math.pi / 180
    lon *= math.pi / 180
    x = math.cos(lat) * math.cos(lon)
    z = math.cos(lat) * math.sin(lon)
    y = math.sin(lat)
    return [x, y, z]


def main():
    vmin, vmax = 0.1, 03
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
        xs.append(lon)
        ys.append(lat)
        ts.append(t)
 

    lons = np.arange(-180, 180, 0.25)
    lats = np.arange(-90, 90, 0.25)
    X, Y = np.meshgrid(lons, lats)
    Z = np.zeros(X.shape)
    count = 0
    for i, _ in np.ndenumerate(Z):
        lon, lat = X[i], Y[i]

    print 'plotting'
    maps = [
        ('nyc', (20, 20), basemap.Basemap(projection='ortho',lat_0=30,lon_0=-30,resolution='l')),
        ('asia', (20, 20), basemap.Basemap(projection='ortho',lat_0=23,lon_0=105,resolution='l')),
        ('world', (20, 10), basemap.Basemap(projection='cyl', llcrnrlat=-60,urcrnrlat=80,\
                                           llcrnrlon=-180,urcrnrlon=180,resolution='c'))
    ]
    Z = basemap.maskoceans(X, Y, Z, resolution='h', grid=1.25)
    for k, figsize, m in maps:
        print 'drawing', k
        plt.figure(figsize=figsize)

        # draw coastlines, country boundaries, fill continents.
        m.drawcoastlines(linewidth=0.25)
        m.drawcountries(linewidth=0.25)

        # draw lon/lat grid lines every 30 degrees.
        m.drawmeridians(np.arange(0,360,30))
        m.drawparallels(np.arange(-90,90,30))

        # contour data over the map.
        cf = m.contourf(X, Y, Z, 20, cmap=plt.get_cmap('magma'), norm=plt.Normalize(vmin=vmin, vmax=vmax), latlon=True)
        cbar = m.colorbar(cf)
        cbar.set_label('ping round trip time (s)', rotation=270)

        plt.savefig(k + '.png', bbox_inches='tight')



if __name__ == '__main__':
    main()
