import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from time_series import *
from read_data_sets import *


noaa_version = "v4.0.1.201710"
hadcrut_version = "4.6.0.0"
cw_version = "v2_0_0"

plotpre = False

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



pre_had  = had_ts.calculate_average(1880,1900)
pre_ncdc = ncdc_ts.calculate_average(1880,1900)
pre_giss = giss_ts.calculate_average(1880,1900)

preindus_mid  = 1.0 + (pre_giss+pre_had+pre_ncdc)/3.0

print pre_had,pre_ncdc,pre_giss,(pre_giss+pre_had+pre_ncdc)/3.0

for w in [5, 10]:
    hfont = {'fontname':'Arial'}

    plt.figure(figsize=(16,9))

    if plotpre:
        plt.plot([1781,1859],[preindus_mid, preindus_mid],color="Powderblue")
        plt.plot([1904,2023],[preindus_mid, preindus_mid],color="Powderblue")
    
#    cw5, cwax = cw_ts.plot_running_line(w,'pink')
#    berk5, berkax = berk_ts.plot_running_line(w,'grey')
    jra5, jrax = jra_ts.plot_running_line(w,'mediumorchid')
    era5, erax = era_ts.plot_running_line(w,'forestgreen')
    had5, hadax = had_ts.plot_running_line(w,'indianred')
    gis5, gisax = giss_ts.plot_running_line(w,'darkorange')
    ncd5, ncdax = ncdc_ts.plot_running_line(w,'steelblue')

    print (w,jra5[-1],era5[-1],had5[-1],gis5[-1],ncd5[-1],
           np.mean([jra5[-1],era5[-1],had5[-1],gis5[-1],ncd5[-1]]))

    print (w,jra5[-2],era5[-2],had5[-2],gis5[-2],ncd5[-2],
           np.mean([jra5[-2],era5[-2],had5[-2],gis5[-2],ncd5[-2]]))

    print (w,jra5[-3],era5[-3],had5[-3],gis5[-3],ncd5[-3],
           np.mean([jra5[-3],era5[-3],had5[-3],gis5[-3],ncd5[-3]]))

    fsz = 18
    
    if plotpre:
        plt.text(1861, 0.348, '~1$^\circ$C above pre-industrial', fontdict=hfont, fontsize=fsz, color="powderblue")
    

    plt.xlabel('Year', fontsize=fsz, **hfont)
    plt.ylabel('Anomaly relative to 1981-2010 ($^\circ$C)', fontsize=fsz, **hfont)
    
#plt.legend(loc='lower right', frameon=False)
    plt.legend(bbox_to_anchor=(0.89, 0.42),
               bbox_transform=plt.gcf().transFigure, 
               frameon=False)
    
    plt.xticks(range(1860,2040,20), fontsize = fsz, **hfont)
    plt.yticks(np.arange(-1.2,1.0,0.2), fontsize = fsz, **hfont)
    plt.axis((1845,2022.5,-1.1,0.7))
    
    ax1 = plt.axes()
    ax1.set_frame_on(False)
    ax1.yaxis.set_ticks_position('left')
    ax1.xaxis.set_ticks_position('bottom')
    
    sw = str(w)

    plt.title(sw+'-year Global temperature anomaly 1850-2017', loc='left', fontsize = fsz+10, **hfont)

    plt.savefig('Figures/gmt_'+sw+'y.png', bbox_inches='tight')


hfont = {'fontname':'Arial'}
plt.figure(figsize=(16,9))
combined = had_ts.combine([jra_ts,era_ts,ncdc_ts,giss_ts])
combined.plot_running_mean([5])
plt.plot([1781,1859],[preindus_mid, preindus_mid],color="Powderblue")
plt.plot([1904,2023],[preindus_mid, preindus_mid],color="Powderblue")
fsz = 18
plt.text(1861, 0.348, '~1$^\circ$C above pre-industrial', fontdict=hfont, fontsize=fsz, color="powderblue")
plt.xlabel('Year', fontsize=fsz, **hfont)
plt.ylabel('Anomaly relative to 1981-2010 ($^\circ$C)', fontsize=fsz, **hfont)
plt.xticks(range(1860,2040,20), fontsize = fsz, **hfont)
plt.yticks(np.arange(-1.2,1.0,0.2), fontsize = fsz, **hfont)
plt.axis((1845,2022.5,-1.1,0.7))  
ax1 = plt.axes()
ax1.set_frame_on(False)
ax1.yaxis.set_ticks_position('left')
ax1.xaxis.set_ticks_position('bottom')
plt.title(sw+'-year Global temperature anomaly 1850-2017', loc='left', fontsize = fsz+10, **hfont)
plt.savefig('Figures/gmt_5yr_skyscraper.png', bbox_inches='tight')
 
