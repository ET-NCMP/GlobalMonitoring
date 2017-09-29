import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.patches import Polygon
from time_series import *
from read_data_sets import *
import matplotlib.patches as mpatches

noaa_version = "v4.0.1.201707"
hadcrut_version = "4.6.0.0"


print("GLOBAL AVERAGE TEMPERATURES")

had_ts = read_hadcrut4(hadcrut_version)
had_ts.add_name("HadCRUT."+hadcrut_version)
had_ts.rebaseline(1880,1900)

ncdc_monthly = read_ncdc_monthly(noaa_version)
ncdc_monthly.rebaseline(1880,1900)
ncdc_ts = ncdc_monthly.annualise()
ncdc_ts.add_name("NOAAGlobalTemp")

giss_monthly = read_giss_monthly()
giss_monthly.rebaseline(1880,1900)
giss_ts = giss_monthly.annualise()
giss_ts.add_name("GISTEMP")

had_mean = had_ts.calculate_average(1981,2010)
ncdc_mean = ncdc_ts.calculate_average(1981,2010)
giss_mean = giss_ts.calculate_average(1981,2010)

avg_clim = ( had_mean + ncdc_mean + giss_mean )/3.

jra_monthly = read_jra55()
jra_monthly.rebaseline(1981,2010)
jra_ts = jra_monthly.annualise()
jra_ts.add_name("JRA-55")
jra_ts.add_offset(avg_clim)


era_monthly = read_era_interim()
era_monthly.rebaseline(1981,2010)
era_ts = era_monthly.annualise()
era_ts.add_name("ERA-interim")
era_ts.add_offset(avg_clim)

print had_ts.get_value(2015) - had_ts.calculate_average(1880,1900)
print had_ts.get_value(2016) - had_ts.calculate_average(1880,1900)
print had_ts.calculate_average(2010,2016) - had_ts.calculate_average(1880,1900)

hfont = {'fontname':'Arial'}

plt.figure(figsize=(16,9))

jra_ts.plot_ts('mediumorchid')
era_ts.plot_ts('forestgreen')
had_ts.plot_ts_with_unc('indianred','lightyellow')
giss_ts.plot_ts('darkorange')
ncdc_ts.plot_ts('steelblue')

fsz = 18

plt.xlabel('Year', fontsize=fsz, **hfont)
plt.ylabel('Anomaly relative to 1880-1900 ($^\circ$C)', fontsize=fsz, **hfont)

#plt.legend(loc='upper left', frameon=False)
plt.legend(bbox_to_anchor=(0.3, 0.87),
           bbox_transform=plt.gcf().transFigure, 
           frameon=False)

plt.xticks(range(1860,2040,20), fontsize = fsz, **hfont)
plt.yticks(np.arange(-0.5,1.5,0.25), fontsize = fsz, **hfont)
plt.axis((1845,2022.5,-0.43,1.33))

ax1 = plt.axes()
ax1.set_frame_on(False)
ax1.yaxis.set_ticks_position('left')
ax1.xaxis.set_ticks_position('bottom')

plt.title('Global mean temperature 1850-2017', loc='left', fontsize = fsz+10, **hfont)

plt.savefig('Figures/gmt_pre.png', bbox_inches='tight')
#plt.show()

jra_ts.print_ordered_ts(5)
era_ts.print_ordered_ts(5)
had_ts.print_ordered_ts(5)
ncdc_ts.print_ordered_ts(5)
giss_ts.print_ordered_ts(5)

