#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl
from mpl_toolkits.basemap import Basemap

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# lat_ts is the latitude of true scale.
# resolution = 'c' means use crude resolution coastlines.
pl.clf()
m = Basemap(projection='merc', llcrnrlat=-80, urcrnrlat=80, \
            llcrnrlon=-180, urcrnrlon=180, lat_ts=20, resolution='c')
m.drawcoastlines()
m.fillcontinents(color='coral', lake_color='aqua')
# draw parallels and meridians.
m.drawparallels(np.arange(-90., 91., 30.))
m.drawmeridians(np.arange(-180., 181., 60.))
m.drawmapboundary(fill_color='aqua')
m.drawstates()
pl.title("Mercator Projection")
pl.show()

pl.savefig('basemap.png')