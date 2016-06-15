import math

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
