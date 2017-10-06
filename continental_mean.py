import numpy as np
import read_data_sets as rd
import matplotlib.pyplot as plt

goodnames = ['Africa','Asia','Europe','North America','Oceania','South America']

for i,country in enumerate(["africa","asia","europe","northAmerica","oceania","southAmerica"]):

    ts = rd.read_noaa_continents(country)
    ts.rebaseline(1981,2010)
    ts.add_name(country)

    ts.print_ts()
    ts.print_ordered_ts(10)

    hfont = {'fontname':'Arial'}
    plt.figure(figsize=(16,9))

    ts.plot_ts('red')

    fsz = 18

    plt.xlabel('Year', fontsize=fsz, **hfont)
    plt.ylabel('Anomaly relative to 1981-2010 ($^\circ$C)', fontsize=fsz, **hfont)

    plt.xticks(range(1920,2040,20), fontsize = fsz, **hfont)
    plt.yticks(np.arange(-2.0,1.75,0.5), fontsize = fsz, **hfont)
    plt.axis((1905,2022.5,-2.03,1.53))

    ax1 = plt.axes()
    ax1.set_frame_on(False)
    ax1.yaxis.set_ticks_position('left')
    ax1.xaxis.set_ticks_position('bottom')

    plt.title('Continental temperature anomaly for '+goodnames[i]+' 1910-2017', loc='left', fontsize = fsz+10, **hfont)
    
    plt.savefig('Figures/'+country+'.png', bbox_inches='tight')


