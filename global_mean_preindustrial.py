import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.patches import Polygon
from time_series import *
from read_data_sets import *
import matplotlib.patches as mpatches

noaa_version = "v4.0.1.201712"
hadcrut_version = "4.6.0.0"

clim1=1850
clim2=1900

print("GLOBAL AVERAGE TEMPERATURES")

had_ts = read_hadcrut4(hadcrut_version)
had_ts.add_name("HadCRUT."+hadcrut_version)
had_ts.rebaseline(clim1,clim2)

had_early_mean = had_ts.calculate_average(1880,1900)

#ncdc_monthly = read_all(3)
ncdc_monthly = read_ncdc_monthly(noaa_version)
ncdc_monthly.rebaseline(1880,1900)
ncdc_ts = ncdc_monthly.annualise()
ncdc_ts.add_name("NOAAGlobalTemp")
ncdc_ts.add_offset(had_early_mean)

#giss_monthly = read_all(1)
giss_monthly = read_giss_monthly()
giss_monthly.rebaseline(1880,1900)
giss_ts = giss_monthly.annualise()
giss_ts.add_name("GISTEMP")
giss_ts.add_offset(had_early_mean)

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
era_ts.add_name("ERA-Interim")
era_ts.add_offset(avg_clim)


jra_ts.print_to_file_nounc('JRA_global_mean_1880_1900.csv')
era_ts.print_to_file_nounc('ERA_global_mean_1880_1900.csv')
had_ts.print_to_file_nounc('HadCRUT_global_mean_1880_1900.csv')
ncdc_ts.print_to_file_nounc('NOAAGlobalTemp_global_mean_1880_1900.csv')
giss_ts.print_to_file_nounc('GISTEMP_global_mean_1880_1900.csv')


print had_ts.get_value(2015) - had_ts.calculate_average(1880,1900)
print had_ts.get_value(2016) - had_ts.calculate_average(1880,1900)
print had_ts.calculate_average(2010,2016) - had_ts.calculate_average(1880,1900)

hfont = {'fontname':'Arial'}

plt.figure(figsize=(16,9))

jra_ts.plot_ts('mediumorchid')
era_ts.plot_ts('forestgreen')
had_ts.plot_ts('indianred')
giss_ts.plot_ts('darkorange')
ncdc_ts.plot_ts('steelblue')

fsz = 18

plt.xlabel('Year', fontsize=fsz, **hfont)
plt.ylabel('Anomaly relative to 1850-1900 ($^\circ$C)', fontsize=fsz, **hfont)

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

plt.title('Global temperature anomaly 1850-2017 relative to pre-industrial', loc='left', fontsize = fsz+10, **hfont)

#plt.savefig('Figures/gmt_pre.png', bbox_inches='tight')
plt.savefig('Figures/gmt_pre.eps', bbox_inches='tight')
#plt.show()

jra_ts.print_ordered_ts(5)
era_ts.print_ordered_ts(5)
had_ts.print_ordered_ts(5)
ncdc_ts.print_ordered_ts(5)
giss_ts.print_ordered_ts(5)

print "Averages for various years"
for y in range(1998,2018):

    av = (had_ts.get_value(y) +
          jra_ts.get_value(y) +
          era_ts.get_value(y) +
          ncdc_ts.get_value(y) +
          giss_ts.get_value(y))/5.
    print y,av, np.std([had_ts.get_value(y),
                        jra_ts.get_value(y),
                        era_ts.get_value(y),
                        ncdc_ts.get_value(y),
                        giss_ts.get_value(y)]) * 1.96

av = np.mean([had_ts.get_value(2017),
              jra_ts.get_value(2017),
              era_ts.get_value(2017),
              ncdc_ts.get_value(2017),
              giss_ts.get_value(2017)])

print np.std([had_ts.get_value(2017),
              jra_ts.get_value(2017),
              era_ts.get_value(2017),
              ncdc_ts.get_value(2017),
              giss_ts.get_value(2017)]) * 1.96
print av

jra5, jrax = jra_ts.plot_running_line(5,'mediumorchid')
era5, erax = era_ts.plot_running_line(5,'forestgreen')
had5, hadax = had_ts.plot_running_line(5,'indianred')
gis5, gisax = giss_ts.plot_running_line(5,'darkorange')
ncd5, ncdax = ncdc_ts.plot_running_line(5,'steelblue')

print "5 year averages wrt pre-industrial"
print jra5[-1],era5[-1],had5[-1],gis5[-1],ncd5[-1]
print np.mean([jra5[-1],era5[-1],had5[-1],gis5[-1],ncd5[-1]])
