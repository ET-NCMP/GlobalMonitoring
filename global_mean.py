import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from time_series import *
from read_data_sets import *


noaa_version = "v4.0.1.201712"
hadcrut_version = "4.6.0.0"
cw_version = "v2_0_0"

plotpre = True

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

ncdc_monthly = read_all(3)
#ncdc_monthly = read_ncdc_monthly(noaa_version)
ncdc_monthly.rebaseline(1981,2010)
ncdc_ts = ncdc_monthly.annualise()
ncdc_ts.add_name("NOAAGlobalTemp")

giss_monthly = read_all(1)
#giss_monthly = read_giss_monthly()
giss_monthly.rebaseline(1981,2010)
giss_ts = giss_monthly.annualise()
giss_ts.add_name("GISTEMP")

berk_monthly = read_berkeley()
berk_monthly.rebaseline(1981,2010)
berk_ts = berk_monthly.annualise()
berk_ts.add_name("BerkeleyEarth")

cw_monthly = read_cowtan_and_way_monthly(cw_version)
cw_monthly.rebaseline(1981,2010)
cw_ts = cw_monthly.annualise()
cw_ts.add_name("Cowtan and Way")

#mrlk = read_mrlk()
#mrlk.rebaseline(1981,2010)
#mrlk.add_name("MRLK")

jra_ts.print_to_file_nounc('JRA_global_mean_1981_2010.csv')
era_ts.print_to_file_nounc('ERA_global_mean_1981_2010.csv')
had_ts.print_to_file_nounc('HadCRUT_global_mean_1981_2010.csv')
ncdc_ts.print_to_file_nounc('NOAAGlobalTemp_global_mean_1981_2010.csv')
giss_ts.print_to_file_nounc('GISTEMP_global_mean_1981_2010.csv')


print "Difference in baseline 1981-2010 minus 1961-1990"
hadclimshift= had_ts.calculate_average(1981,2010)-had_ts.calculate_average(1961,1990)
ncdcclimshift = ncdc_ts.calculate_average(1981,2010)-ncdc_ts.calculate_average(1961,1990)
gissclimshift = giss_ts.calculate_average(1981,2010)-giss_ts.calculate_average(1961,1990)
print hadclimshift,ncdcclimshift,gissclimshift
print (hadclimshift+ncdcclimshift+gissclimshift)/3.

print "Difference in baseline 1981-2010 minus 1880-1900"
hadclimshift= had_ts.calculate_average(1981,2010)-had_ts.calculate_average(1880,1900)
ncdcclimshift = ncdc_ts.calculate_average(1981,2010)-ncdc_ts.calculate_average(1880,1900)
gissclimshift = giss_ts.calculate_average(1981,2010)-giss_ts.calculate_average(1880,1900)
print hadclimshift,ncdcclimshift,gissclimshift
print (hadclimshift+ncdcclimshift+gissclimshift)/3.

print "Difference in baseline 1986-2005 minus 1981-2010"
hadclimshift= had_ts.calculate_average(1986,2005)-had_ts.calculate_average(1981,2010)
ncdcclimshift = ncdc_ts.calculate_average(1986,2005)-ncdc_ts.calculate_average(1981,2010)
gissclimshift = giss_ts.calculate_average(1986,2005)-giss_ts.calculate_average(1981,2010)
print hadclimshift,ncdcclimshift,gissclimshift
print (hadclimshift+ncdcclimshift+gissclimshift)/3.

pre_had  = had_ts.calculate_average(1880,1900)
pre_ncdc = ncdc_ts.calculate_average(1880,1900)
pre_giss = giss_ts.calculate_average(1880,1900)

preindus_mid  = 1.0 + (pre_giss+pre_had+pre_ncdc)/3.0
preindus_low  = preindus_mid - 0.1
preindus_high = preindus_mid + 0.1

hfont = {'fontname':'Arial'}

plt.figure(figsize=(16,9))

#plt.fill_between([1781,2023],[preindus_low, preindus_low],[preindus_high, preindus_high],
#                 facecolor="Powderblue",color="Powderblue", alpha=0.15,
#                label='1 sigma range')
if plotpre:
    plt.plot([1781,1859],[preindus_mid, preindus_mid],color="Powderblue")
    plt.plot([1904,2023],[preindus_mid, preindus_mid],color="Powderblue")
#plt.plot([1781,2023],[preindus_low, preindus_low],color="Powderblue")
#plt.plot([1781,2023],[preindus_high, preindus_high],color="Powderblue")

#mrlk.plot_ts_with_unc('silver','silver')
cw_ts.plot_ts('pink')
berk_ts.plot_ts('grey')
jra_ts.plot_ts('mediumorchid')
era_ts.plot_ts('forestgreen')
had_ts.plot_ts('indianred')
giss_ts.plot_ts('darkorange')
ncdc_ts.plot_ts('steelblue')

#mrlk.add_name("MRLK mean")
#mrlk.plot_ts('black')

fsz = 18

if plotpre:
    plt.text(1861, 0.348, '~1$^\circ$C above pre-industrial', fontdict=hfont, fontsize=fsz, color="powderblue")


plt.xlabel('Year', fontsize=fsz, **hfont)
plt.ylabel('Anomaly relative to 1981-2010 ($^\circ$C)', fontsize=fsz, **hfont)

#plt.legend(loc='lower right', frameon=False)
plt.legend(bbox_to_anchor=(0.89, 0.38),
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

jra_ts.print_ordered_ts(10)
era_ts.print_ordered_ts(10)
had_ts.print_ordered_ts(10)
ncdc_ts.print_ordered_ts(10)
giss_ts.print_ordered_ts(10)

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
    

av = (had_ts.get_value(2017) +
      jra_ts.get_value(2017) +
      era_ts.get_value(2017) +
      ncdc_ts.get_value(2017) +
      giss_ts.get_value(2017))/5.


print "Average of global mean series for 2017 and 95% range"
print av
print np.std([had_ts.get_value(2017),
              jra_ts.get_value(2017),
              era_ts.get_value(2017),
              ncdc_ts.get_value(2017),
              giss_ts.get_value(2017)]) * 1.96


