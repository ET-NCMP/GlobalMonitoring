import numpy as np
import struct
from time_series import *
import csv


def read_co2():

    timeax  = []
    data = []

#https://www.esrl.noaa.gov/gmd/ccgg/trends/full.html
    with open('Data/co2_mm_mlo.txt','rb') as infile:
        for i in range(1,73):
            infile.readline()
        for line in infile:
            columns = line.split()
            timeax.append(float(columns[2]))
            co2 = float(columns[3])
            if co2 == -99.99:
                co2  = None
            data.append(co2)

    return timeax,data

def read_ohc():

    timeax = []
    anoms = []
    lower_unc = []
    upper_unc = []

#https://data.nodc.noaa.gov/woa/DATA_ANALYSIS/3M_HEAT_CONTENT/DATA/basin/yearly/h22-w0-700m.dat
    with open('Data/h22-w0-700m.dat', 'rb') as infile:
        infile.readline()
        for line in infile:
            columns = line.split()
            timeax.append(float(columns[0])-0.5)
            anoms.append(float(columns[1]))
            lower_unc.append(float(columns[1])-2*float(columns[2]))
            upper_unc.append(float(columns[1])+2*float(columns[2]))

    ts = time_series(timeax,
                     anoms,
                     lower_unc,
                     upper_unc)

    return ts

def read_mohc_ohc():

    timeax = []
    anoms = []
    lower_unc = []
    upper_unc = []

#from Rachel Killick
    with open('Data/MOHC-TimeSeries-700m_19502017_.txt', 'rb') as infile:
        infile.readline()
        for line in infile:
            columns = line.split()
            timeax.append(float(columns[0]))
            anoms.append(float(columns[1])/1E22)
            lower_unc.append((float(columns[1])-2*float(columns[2]))/1E22)
            upper_unc.append((float(columns[1])+2*float(columns[2]))/1E22)

        ts = time_series(timeax,
                         anoms,
                         lower_unc,
                         upper_unc)

    return ts

def read_noaa_continents(continent):

    years = []
    anoms = []
    anomsl = []
    anomsh = []

    with open('Data/'+continent+'_1880-2017.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    
        count = 0
        for row in reader:
            count+=1
            if count > 5:
                years.append(float(row[0]))
                anoms.append(float(row[1]))
                anomsl.append(float(row[1]))
                anomsh.append(float(row[1]))

    ts = time_series(years,anoms,anomsl,anomsh)

    return ts

def read_sea_level():

    f = open('Data/GMSL_TPJOAS_V4_199209_201706.txt' ,'r')

    for i in range(1,45):
        f.readline()

    timeax = []
    sealevel = []

    for line in f:
        line = line.strip()
        columns = line.split()
        timeax.append(float(columns[2]))
        sealevel.append(float(columns[11]))

    f.close()

    return timeax, sealevel

def read_CSIRO_sea_level():

    f = open('Data/CSIRO_Alt.csv' ,'r')

    f.readline()

    timeax = []
    sealevel = []

    for line in f:
        line = line.strip()
        columns = line.split(',')

        timeax.append(float(columns[0]))
        sealevel.append(float(columns[1]))

    f.close()

    return timeax, sealevel

def read_mrlk():

    f = open('/project/earthobs/GLOBAL_SURFACE_TEMPERATURE/MRLK/annavg2decdata.txt','r')
    f.readline()
    
    mrlk_year = []
    mrlk_anom = []
    mrlk_upper_unc = []
    mrlk_lower_unc = []

    year = 1850
    for line in f:
        columns = line.split()
        columns = columns[1:]
        columns = map(float, columns)

        mrlk_year.append(year)
        mrlk_anom.append(np.mean(columns))
        mrlk_upper_unc.append(np.mean(columns)+2*np.std(columns))
        mrlk_lower_unc.append(np.mean(columns)-2*np.std(columns))

        year += 1

    f.close()

    return time_series(mrlk_year, mrlk_anom, mrlk_upper_unc, mrlk_lower_unc)


def read_mrlk_stream(nstream):

    for i in range(nstream):
        f = open('/project/earthobs/GLOBAL_SURFACE_TEMPERATURE/MRLK/annavg2decdata.txt','r')
        f.readline()
        
        mrlk_year = []
        mrlk_anom = []
        mrlk_upper_unc = []
        mrlk_lower_unc = []

        year = 1850
        for line in f:
            columns = line.split()
            columns = columns[1:]
            columns = map(float, columns)

            mrlk_year.append(year)
            mrlk_anom.append(columns[i])
            mrlk_upper_unc.append(columns[i])
            mrlk_lower_unc.append(columns[i])

            year += 1

        f.close()

        yield time_series(mrlk_year, mrlk_anom, mrlk_upper_unc, mrlk_lower_unc)


def read_berkeley():

    f = open('Data/Land_and_Ocean_complete.txt','r')
    for i in range(1,78):
        f.readline()

    anoms = []
    years = []
    months = []

    for line in f:
        line = line.strip()
        if line == "":
            break

        columns = line.split()

        anoms.append(float(columns[2]))
        years.append(float(columns[0]))
        months.append(float(columns[1]))

    f.close()

    return monthly_time_series(years,months,anoms)

def slices(s, *args):
    position = 0
    splits = []
    for length in args:
        splits.append(s[position:position + length])
        position += length
    return splits



def read_psd(filename):

    f = open(filename,'r')

    line = f.readline()
    line = line.strip()
    line = line.split()

    year1 = float(line[0])
    year2 = float(line[1])

    year = []
    month = []
    data = []

    readon = 1

    for line in f:
        if readon == 1:
            line = line.strip()
            line = line.split()

            for i in range(1,13):
                if float(line[i]) != -99.99:
                    year.append(float(line[0]))
                    month.append(float(i))
                    data.append(float(line[i]))

            if float(line[0]) == year2:
                readon = 0


    f.close()
    
    psd = monthly_time_series(year,month,data)
    return psd


    
def read_jra55():
    f=open("Data/JRA-55_tmp2m_global_ts_Clim8110.txt",'r')

    jra_year = []
    jra_month = []
    jra_data = []

    for line in f:
        line = line.strip()
        jra_year.append(float(line[0:4]))
        jra_month.append(float(line[5:7]))
        jra_data.append(float(line[8:]))

    f.close()

    jra_ts = monthly_time_series(jra_year, jra_month, jra_data)

    return jra_ts
    

def read_era_interim():
    f=open("Data/ts_1month_anom_ei_T2_197901-201712.txt",'r')

    f.readline()
    f.readline()
    f.readline()
    f.readline()

    era_year = []
    era_month = []
    era_data = []

    for line in f:
        line = line.strip()
        cols = line.split(',')
        era_year.append(float(line[0:4]))
        era_month.append(float(line[4:6]))
        era_data.append(float(cols[1]))

    f.close()

    era_ts = monthly_time_series(era_year, era_month, era_data)

    return era_ts

 
def read_hadsst3_monthly(version):
    return read_hadley_monthly('Data/HadSST.'+version+'_monthly_globe_ts.txt')
 
def read_hadcrut4_monthly(version):
    return read_hadley_monthly('Data/HadCRUT.'+version+'.monthly_ns_avg.txt')

def read_hadley_monthly(filename):
#read hadley format monthly datasets and make an annual time series out of them
    f = open(filename,'r')

    years = []
    months = []
    data = []
    lounc = []
    hiunc = []

    for line in f:

        line = line.strip()
        columns = line.split()
        yd = columns[0].split('/')

        years.append(float(yd[0]))
        months.append(float(yd[1]))
        data.append(float(columns[1]))
        lounc.append(float(columns[10]))
        hiunc.append(float(columns[11]))

    f.close()

    return monthly_time_series_with_uncertainty(years,months,data,lounc,hiunc)
    
def read_hadley_monthly_bias(filename):
#read hadley format monthly datasets and make an annual time series out of them
    f = open(filename,'r')

    years = []
    months = []
    data = []
    lounc = []
    hiunc = []

    for line in f:

        line = line.strip()
        columns = line.split()
        yd = columns[0].split('/')

        years.append(float(yd[0]))
        months.append(float(yd[1]))
        data.append(float(columns[1]))
        lounc.append(float(columns[2]))
        hiunc.append(float(columns[3]))

    f.close()

    return monthly_time_series_with_uncertainty(years,months,data,lounc,hiunc)
    

def read_hadley(filename):
#read hadley format annual data sets and make annual time series out of them
    f = open(filename, 'r')

    hadcrut_year = []
    hadcrut_anom = []
    hadcrut_upper_unc = []
    hadcrut_lower_unc = []

    # Loop over lines and extract variables of interest
    for line in f:
        line = line.strip()
        columns = line.split()
        hadcrut_year.append(float(columns[0]))
        hadcrut_anom.append(float(columns[1]))
        hadcrut_upper_unc.append(float(columns[11]))
        hadcrut_lower_unc.append(float(columns[10]))
    
    f.close()
    had_ts = time_series(hadcrut_year,
                         hadcrut_anom,
                         hadcrut_lower_unc,
                         hadcrut_upper_unc)

    return had_ts

def read_hadley_bias(filename):
#read hadley format annual data sets and make annual time series out of them
    f = open(filename, 'r')

    hadcrut_year = []
    hadcrut_anom = []
    hadcrut_upper_unc = []
    hadcrut_lower_unc = []

    # Loop over lines and extract variables of interest
    for line in f:
        line = line.strip()
        columns = line.split()
        hadcrut_year.append(float(columns[0]))
        hadcrut_anom.append(float(columns[1]))
        hadcrut_upper_unc.append(float(columns[3]))
        hadcrut_lower_unc.append(float(columns[2]))
    
    f.close()
    had_ts = time_series(hadcrut_year,
                         hadcrut_anom,
                         hadcrut_lower_unc,
                         hadcrut_upper_unc)

    return had_ts


def read_hadcrut4(version):
    return read_hadley('Data/HadCRUT.'+version+'.annual_ns_avg.1981-2010.txt')


def read_ncei_binary(filename,timepoints,y1):

    file = open(filename,'rb')
    fileContent = file.read()

    years = []
    months = []
    data = []
    lounc = []
    hiunc = []

    yyy = y1
    mmm = 1
    for i in range(0,timepoints):
        a,b = struct.unpack(">ff", fileContent[i*8:i*8+8])

        years.append(yyy)
        months.append(mmm)
        data.append(a)
        lounc.append(a-b)
        hiunc.append(a+b)

        mmm += 1
        if mmm > 12:
            mmm = 1
            yyy += 1

    file.close()

    return monthly_time_series_with_uncertainty(years,months,data,lounc,hiunc)


def read_ncdc_format_monthly(filename):
    f = open(filename, 'r')
    ncdc_year = []
    ncdc_month = []
    ncdc_anom = []

    # Loop over lines and extract variables of interest
    for line in f:
        line = line.strip()
        columns = line.split()
        ncdc_year.append(float(columns[0]))
        ncdc_month.append(float(columns[1]) )
        ncdc_anom.append(float(columns[2]))

    f.close()

    ncdc_ts = monthly_time_series(ncdc_year,
                                  ncdc_month,
                                  ncdc_anom)

    return ncdc_ts
    
def read_ncdc_monthly(version):
    return read_ncdc_format_monthly('Data/aravg.mon.land_ocean.90S.90N.'+version+'.asc')

def read_ncdc_ocean_monthly(version):
    return read_ncdc_format_monthly('Data/aravg.mon.land_ocean.90S.90N.'+version+'.asc')


def read_alt_ncdc_monthly():
    filename = 'Data/monthly.land_ocean.90S.90N.df_1901-2000mean.dat'
    return read_alt_ncdc_monthly_format(filename)

def read_alt_ncdc_lsat_monthly():
    filename = 'Data/monthly.land.90S.90N.df_1901-2000mean.dat'
    return read_alt_ncdc_monthly_format(filename)

def read_alt_ncdc_sst_monthly():
    filename = 'Data/monthly.ocean.90S.90N.df_1901-2000mean.dat'
    return read_alt_ncdc_monthly_format(filename)

def read_alt_ncdc_monthly_format(filename):
    f = open(filename,'r')

    ncdc_year = []
    ncdc_month = []
    ncdc_anom = []
    for line in f:
        line = line.strip()
        columns = line.split()
        if float(columns[2]) > -99.0000:
            ncdc_year.append(float(columns[0]))
            ncdc_month.append(float(columns[1]) )
            ncdc_anom.append(float(columns[2]))

    f.close()

    
    ncdc_ts = monthly_time_series(ncdc_year,
                                  ncdc_month,
                                  ncdc_anom)

    return ncdc_ts

def read_ncdc_format(filename):
    f = open(filename, 'r')
    ncdc_year = []
    ncdc_anom = []
    ncdc_lounc = []
    ncdc_hiunc = []

    # Loop over lines and extract variables of interest
    for line in f:
        line = line.strip()
        columns = line.split()
        ncdc_year.append(float(columns[0]))
        ncdc_anom.append(float(columns[1]))
        ncdc_lounc.append(float(columns[1]) - 2 * np.sqrt(float(columns[2])) )
        ncdc_hiunc.append(float(columns[1]) + 2 * np.sqrt(float(columns[2])) )

    f.close()

    ncdc_ts = time_series(ncdc_year,
                          ncdc_anom,
                          ncdc_lounc,
                          ncdc_hiunc)

    return ncdc_ts


def read_all(col):

    years = []
    months = []
    anoms = []

    with open('Data/all.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        month = 1

        count = 0
        for row in reader:
            count+=1
            if count > 1:
                if float(row[col]) > -90.0:
                    years.append(int(float(row[0])))
                    anoms.append(float(row[col]))
                    months.append(month)

                    month += 1
                    if month == 13:
                        month = 1
            else:
                print row[col]


    ts = monthly_time_series(years,
                             months,
                             anoms)
    return ts


def read_ncdc(version):
    return read_ncdc_format('Data/aravg.ann.land_ocean.90S.90N.'+version+'.asc')


def read_giss_block_monthly(f, block_length, giss_year, giss_month, giss_anom):
#burn first two pointless lines of each block
    line = f.readline()
    line = f.readline()
    for j in range(1,block_length+1):
        line = f.readline()
        columns = line.split()
        for i in range(1,13):
            giss_year.append(float(columns[0]))
            giss_month.append(float(i))
            giss_anom.append(float(columns[i])/100.)
            
    return (giss_year, giss_month, giss_anom)

def read_giss_monthly():
    f = open('Data/GLB.Ts+dSST.txt','r')

    giss_year = []
    giss_month = []
    giss_anom = []
  
#read header information and discard
    for i in range(1,7):
        f.readline()

#read first block of 21 years
    giss_year, giss_month, giss_anom = read_giss_block_monthly(f, 21, giss_year, giss_month, giss_anom)
#read five blocks of 20 years   
    for i in range(1,6):
        giss_year, giss_month, giss_anom = read_giss_block_monthly(f, 20, giss_year, giss_month, giss_anom)
#final block has less than 20
    giss_year, giss_month, giss_anom = read_giss_block_monthly(f, 16, giss_year, giss_month, giss_anom)

#final year is incomplete so calculate from monthlies
    g = f.readline()
    columns = g.split()

    for i in range(1,13):
        if columns[i] != '****':
            giss_year.append(float(columns[0]))
            giss_month.append(float(i))
            giss_anom.append(float(columns[i])/100.)
    
    giss_ts = monthly_time_series(giss_year,
                                  giss_month,
                                  giss_anom)

    return giss_ts

def read_giss_block(f, block_length, giss_year, giss_anom):
    line = f.readline()
    line = f.readline()
    for j in range(1,block_length+1):
        line = f.readline()
        columns = line.split()
        giss_year.append(float(columns[0]))
        giss_anom.append(float(columns[13])/100.)
    return (giss_year,giss_anom)


def read_giss():
    f = open('Data/GLB.Ts+dSST.txt','r')
    
    giss_year = []
    giss_anom = []

#read header information and discard
    for i in range(1,7):
        g = f.readline()
        
#read first block of 21 years
    giss_year, giss_anom = read_giss_block(f, 21, giss_year, giss_anom)
#read five blocks of 20 years   
    for i in range(1,6):
        giss_year, giss_anom = read_giss_block(f, 20, giss_year, giss_anom)
#final block has less than 20
    giss_year, giss_anom = read_giss_block(f, 16, giss_year, giss_anom)

#final year is incomplete so calculate from monthlies
    g = f.readline()
    print g
    columns = g.split()
    giss_year.append(float(columns[0]))
    final_year = []
    for i in range(1,13):
        if columns[i] != '****':
            final_year.append(float(columns[i])/100.)
    giss_anom.append(np.mean(final_year))

    giss_lounc = []
    giss_hiunc = []

    for i in range(0,len(giss_year)):
        if giss_year[i] >= 1880 and giss_year[i] <= 1900:
            giss_lounc.append(giss_anom[i]-0.08*1.96)
            giss_hiunc.append(giss_anom[i]+0.08*1.96)
        elif giss_year[i] >= 1901 and giss_year[i] <= 1950:
            giss_lounc.append(giss_anom[i]-0.05*1.96)
            giss_hiunc.append(giss_anom[i]+0.05*1.96)
        elif giss_year[i] >= 1951 and giss_year[i] <= 3000:
            giss_lounc.append(giss_anom[i]-0.05*1.96)
            giss_hiunc.append(giss_anom[i]+0.05*1.96)
    
    giss_ts = time_series(giss_year,
                          giss_anom,
                          giss_lounc,
                          giss_hiunc)

    return giss_ts


def read_cowtan_and_way(version):
    f = open('Data/had4_krig_annual_'+version+'.txt','r')
    
    cw_year = []
    cw_anom = []
    cw_lounc = []
    cw_hiunc = []

    for line in f:
        columns = line.split()
        cw_year.append(int(columns[0]))
        cw_anom.append(float(columns[1]))
        cw_lounc.append(float(columns[1]) - 2* float(columns[2]))
        cw_hiunc.append(float(columns[1]) + 2* float(columns[2]))
        
    cw_ts = time_series(cw_year,
                          cw_anom,
                          cw_lounc,
                          cw_hiunc)

    return cw_ts

def read_cowtan_and_way_monthly(version):
    f = open('Data/had4_krig_'+version+'.txt','r')

    cw_year = []
    cw_month = []
    cw_anom = []

    # Loop over lines and extract variables of interest
    m=1
    for line in f:
        line = line.strip()
        columns = line.split()
        cw_year.append(float(int(float(columns[0]))))
        cw_month.append(m)
        cw_anom.append(float(columns[1]))
        m += 1
        if m == 13:
            m=1

    f.close()

    cw_ts = monthly_time_series(cw_year,
                                cw_month,
                                cw_anom)

    return cw_ts


    f.close()

def read_cowtan_and_way_hybrid_monthly(version):
    f = open('Data/had4_short_uah_'+version+'.txt','r')

    cw_year = []
    cw_month = []
    cw_anom = []

    # Loop over lines and extract variables of interest
    m=1
    for line in f:
        line = line.strip()
        columns = line.split()
        cw_year.append(float(int(float(columns[0]))))
        cw_month.append(m)
        cw_anom.append(float(columns[1]))
        m += 1
        if m == 13:
            m=1

    f.close()

    cw_ts = monthly_time_series(cw_year,
                                cw_month,
                                cw_anom)

    return cw_ts


    f.close()

def read_cowtan_and_way_hybrid(version):
    f = open('Data/had4_short_uah_annual_'+version+'.txt','r')
    
    cw_year = []
    cw_anom = []
    cw_lounc = []
    cw_hiunc = []

    for line in f:
        columns = line.split()
        cw_year.append(int(columns[0]))
        cw_anom.append(float(columns[1]))
        cw_lounc.append(float(columns[1]) - 2* float(columns[2]))
        cw_hiunc.append(float(columns[1]) + 2* float(columns[2]))
        
    cw_ts = time_series(cw_year,
                          cw_anom,
                          cw_lounc,
                          cw_hiunc)

    return cw_ts
