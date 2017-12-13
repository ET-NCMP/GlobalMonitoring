import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from time_series import *
from read_data_sets import *


noaa_version = "v4.0.1.201710"
hadcrut_version = "4.6.0.0"


print("GLOBAL AVERAGE TEMPERATURES")

jra_monthly = read_jra55()
jra_monthly.rebaseline(1981,2010)
jra_ts = jra_monthly.annualise()
jra_ts.add_name("JRA-55")

era_monthly = read_era_interim()
era_monthly.rebaseline(1981,2010)
era_ts = era_monthly.annualise()
era_ts.add_name("ERA-Interim")

had_ts = read_hadcrut4(hadcrut_version)
had_ts.add_name("HadCRUT."+hadcrut_version)
had_ts.rebaseline(1981,2010)

ncdc_monthly = read_ncdc_monthly(noaa_version)
ncdc_monthly.rebaseline(1981,2010)
ncdc_ts = ncdc_monthly.annualise()
ncdc_ts.add_name("NOAAGlobalTemp")

giss_monthly = read_giss_monthly()
giss_monthly.rebaseline(1981,2010)
giss_ts = giss_monthly.annualise()
giss_ts.add_name("GISTEMP")

combined = had_ts.combine([jra_ts,era_ts,ncdc_ts,giss_ts])

combined.plot_skyscraper_diagram()

combined.print_to_file_nounc('WMO_global_mean.csv')

assert False

hfont = {'fontname':'Arial'}

plt.figure(figsize=(16,9))


jra_ts.plot_ts('mediumorchid')
era_ts.plot_ts('forestgreen')
had_ts.plot_ts('indianred')
giss_ts.plot_ts('darkorange')
ncdc_ts.plot_ts('steelblue')

fsz = 18

plt.text(1861, 0.348, '~1$^\circ$C above pre-industrial', fontdict=hfont, fontsize=fsz, color="powderblue")


plt.xlabel('Year', fontsize=fsz, **hfont)
plt.ylabel('Anomaly relative to 1981-2010 ($^\circ$C)', fontsize=fsz, **hfont)

#plt.legend(loc='lower right', frameon=False)
plt.legend(bbox_to_anchor=(0.89, 0.32),
           bbox_transform=plt.gcf().transFigure, 
           frameon=False)

plt.xticks(range(1860,2040,20), fontsize = fsz, **hfont)
plt.yticks(np.arange(-1.2,1.0,0.2), fontsize = fsz, **hfont)
plt.axis((1845,2022.5,-1.1,0.7))

ax1 = plt.axes()
ax1.set_frame_on(False)
ax1.yaxis.set_ticks_position('left')
ax1.xaxis.set_ticks_position('bottom')

plt.title('Global temperature anomaly 1850-2017 relative to 1981-2010', loc='left', fontsize = fsz+10, **hfont)

plt.savefig('Figures/gmt.png', bbox_inches='tight')
#plt.show()


