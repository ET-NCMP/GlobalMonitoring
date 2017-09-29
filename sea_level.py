import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from time_series import *
from read_data_sets import *

ax, sl = read_sea_level()

hfont = {'fontname':'Arial'}
plt.figure(figsize=(16,9))

plt.plot([1992.7, 1992.7],[min(sl),max(sl)],color="Black")
plt.plot([min(ax),max(ax)],[-49,-49],color="Black")

for yy in range(-40,60,20):
    plt.plot([1993,max(ax)],[yy,yy],color="lightgray")
for xx in range(1995,2020,5):
    plt.plot([xx,xx],[min(sl),max(sl)],color="lightgrey")

plt.plot(ax,sl)

fsz = 18
plt.xlabel('Year', fontsize=fsz, **hfont)
plt.ylabel('Height difference from 1996-2015 average (mm)', fontsize=fsz, **hfont)

plt.title('Global mean sea level change 1993 - June 2017', loc='left', fontsize = fsz+5, **hfont)
plt.xticks(range(1990,2025,5), fontsize = fsz, **hfont)
plt.yticks(np.arange(-40,60,20), fontsize = fsz, **hfont)
plt.axis((1992.7,2018,-50,50))

ax1 = plt.axes()
ax1.set_frame_on(False)
ax1.yaxis.set_ticks_position('left')
ax1.xaxis.set_ticks_position('bottom')

plt.text(2002.5,-46,'Data: Beckley et al., 2010, DOI: 10.1080/01490419.2010.491029', fontsize = fsz, **hfont)

plt.savefig('Figures/sl.png', bbox_inches='tight')
#plt.savefig('Figures/sl.eps', bbox_inches='tight')

