import numpy as np
import math
from datetime import date, time, datetime
import calendar
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from math import ceil
from scipy import linalg
from scipy.stats import mode
import random


class monthly_time_series:

    """Class for dealing with monthly time series"""
    
    def __init__(self,years,months,data):
        self.years = years
        self.months = months
        self.data = data
        self.make_time_axis()

    def make_time_axis(self):
#an internal routine that turns year and month into a single time axis
        self.time_axis = self.years[:]
        for i in range(0,len(self.time_axis)):
            self.time_axis[i] += (self.months[i]-1.)/12.

    def add_month(self,year,month,data):
#add a single month to the end of the series
        self.years.append(year)
        self.months.append(month)
        self.data.append(data)
        self.make_time_axis()

    def diff(series1,series2):
#take the difference between the intersection of two series
        n1 = len(series1.data)
        n2 = len(series2.data)

        years = []
        months = []
        data = []

        for i in range(0,n1):
            for j in range(0,n2):
                if series1.years[i] == series2.years[j] and \
                   series1.months[i] == series2.months[j]:
                    years.append(series1.years[i])
                    months.append(series1.months[i])
                    data.append(series1.data[i]-series2.data[j])

        diff = monthly_time_series(years,months,data)
        return diff

    def combine_monthly_series(had,ncdc,giss):
#take an average of three data sets. This is really only going to
#mean anything if those three data sets are HadCRUT, NCDC and GISS
#global temperatures
        comb_year = []
        comb_month = []
        comb_data = []

        for i in range(0,len(ncdc.data)):
            assert ncdc.years[i] == giss.years[i]
            assert ncdc.years[i] == had.years[i+360]
            assert ncdc.months[i] == giss.months[i]
            assert ncdc.months[i] == had.months[i+360]
            comb_year.append(ncdc.years[i])
            comb_month.append(ncdc.months[i])
            comb_data.append(np.mean([ncdc.data[i],giss.data[i],had.data[i+360]]))

        combined = monthly_time_series(comb_year,comb_month,comb_data)

        return combined

    def oplot_ts(self,color):
        plt.plot(self.time_axis,self.data,color=color)

    def plot_ts(self):
#do simple time series plot of monthly series
        plt.plot(self.time_axis,self.data)
        t1 = min(self.time_axis)
        t2 = max(self.time_axis)
        trang = t2-t1
        t1 = t1 - trang*0.02
        t2 = t2 + trang*0.02
        y1 = min(self.data)
        y2 = max(self.data)
        yrang = y2-y1
        y1 = y1 - yrang*0.02
        y2 = y2 + yrang*0.02
        plt.plot([t1,t2],[0,0],color="Black")
        plt.axis((t1,t2,y1,y2))
        plt.xlabel('Year', fontsize=18)
        plt.ylabel('Anomaly relative to 1981-2010 (K)', fontsize=18)
        plt.show()

    def pull_year(self,year):
#extract data for all the months for one specified year
        thisyr = []
        for i in range(0,len(self.data)):
            if self.years[i] == year:
                thisyr.append(self.data[i])
 
        return thisyr

    def pull_month(self,month):
#extract data for all years for one specified month
        thismn = []
        for i in range(0,len(self.data)):
            if self.months[i] == month:
                thismn.append(self.data[i])
 
        return thismn

    def print_ts(self):
        
        for i in range(0,len(self.time_axis)):
            print self.years[i],self.months[i],self.data[i]
        
        return

    def pull_data(self,year,month):
#get data value for a given year and month
        val = -99.
        for i in range(0,len(self.data)):
            if self.years[i] == year and self.months[i]:
                val = self.data[i]
        return val

    def print_month_rank_table(self,nin):
#given an el nino times series, nin, print the
#warmest 10 years for each month
        for m in range(1,13):
            allm = self.pull_month(m)
            allm.sort()
            n = len(allm)
            for rank in range(0,11):
                ind = self.data.index(allm[n-rank])
                nino = nin.pull_data(self.years[ind],self.months[ind])
                print ("%2i %2i %4i %7.3f %7.3f" % (m,rank,self.years[ind],self.data[ind],nino))
            print ("")

    def pull_year_to_date(self, year):
#pull a year of data and then run a cumulative average through it
#returned list first elements is Jan avg, 2nd is Jan-Feb average,
#all the way up to Jan-Dec average (if year goes to December)
        year_to_date = []
        thisyr = self.pull_year(year)

        for i in range(0,len(thisyr)):
            year_to_date.append(np.mean(thisyr[0:i+1]))

        return year_to_date

    def rebaseline(self,year1,year2):
        #choose new climatology period
        clim = np.zeros(12)
        climcounts = np.zeros(12)
        for i in range(0,len(self.years)):
            if self.years[i] >= year1 and self.years[i] <= year2:
                clim[self.months[i]-1] += self.data[i]
                climcounts[self.months[i]-1] += 1.0
        for i in range(0,12):
            clim[i] /= climcounts[i]
        for i in range(0,len(self.years)):
            self.data[i] -= clim[self.months[i]-1]
                       
    def annualise(self, tomonth = 12):
        #go from monthly averages to annual averages
        fyear = int(min(self.years))
        lyear = int(max(self.years))

        annual_years = []
        annual_data = []
        annual_lounc = []
        annual_hiunc = []
        annual_data_ct = []

        for i in range(fyear,lyear+1):
            annual_years.append(0)
            annual_data.append(0)
            annual_lounc.append(0)
            annual_hiunc.append(0)
            annual_data_ct.append(0)

        for i in range(0,len(self.data)):
            if self.months[i] <= tomonth:
                y = int(self.years[i])
                annual_data[y-fyear] += self.data[i]
                annual_data_ct[y-fyear] += 1.0
                annual_years[y-fyear] = y

        for i in range(0,len(annual_data)):
            if annual_data_ct[i] > 0:
                annual_data[i] /= annual_data_ct[i]
                annual_lounc[i] = annual_data[i]
                annual_hiunc[i] = annual_data[i]
            else:
                annual_data[i] =  -99
                annual_lounc[i] =  -99
                annual_hiunc[i] =  -99

        return time_series(annual_years,annual_data,annual_lounc,annual_hiunc)


class monthly_time_series_with_uncertainty(monthly_time_series):

    def __init__(self,years,months,data,lounc,hiunc):
        self.years = years
        self.months = months
        self.data = data
        self.make_time_axis()
        self.lounc = lounc
        self.hiunc = hiunc
        self.name = 'ARG'
        
    def rebaseline(self,year1,year2):
        #choose new climatology period
        clim = np.zeros(12)
        climcounts = np.zeros(12)
        for i in range(0,len(self.years)):
            if self.years[i] >= year1 and self.years[i] <= year2:
                clim[self.months[i]-1] += self.data[i]
                climcounts[self.months[i]-1] += 1.0
        for i in range(0,12):
            clim[i] /= climcounts[i]
        for i in range(0,len(self.years)):
            self.data[i] -= clim[self.months[i]-1]
            self.lounc[i] -= clim[self.months[i]-1]
            self.hiunc[i] -= clim[self.months[i]-1]
    
    def oplot_ts(self,color):
        plt.plot(self.time_axis,self.lounc,color=color)
        plt.plot(self.time_axis,self.hiunc,color=color)

    def oplot_ts_with_uncertainty(self,colora,colorbk):
        
        plt.fill_between(self.time_axis, self.lounc, self.hiunc,
                         facecolor=colorbk,color=colorbk, alpha=0.5,
                         label=self.name)

        


class time_series:

    """class to do annual time series with uncertainty ranges"""

    def __init__(self,times,data,lounc,hiunc):
        self.times = times
        self.data = data
        self.lounc = lounc
        self.hiunc = hiunc
        self.name = ""
   
    def combine(self,others):
        data = []
        data1 = []
        data2 = []
        times = []

        for i, t in enumerate(self.times):
            hold = [self.data[i]]
            for ts in others:
                try:
                    g = ts.get_value(t)
                except:
                    g = None

                if g != None:
                    hold.append(g)

            data.append(np.mean(hold))
            data1.append(max(hold))
            data2.append(min(hold))
            times.append(t)
            
        return time_series(times,data,data1,data2)

    def print_to_file(self,filename):

        file = open(filename,'w')
        for i,time in enumerate(self.times):
            s = (str(int(self.times[i]))+',' +
                 str(round(self.data[i],3 )) +',' +
                 str(round(self.lounc[i],3))+',' +
                 str(round(self.hiunc[i],3))+'\n' )
            file.write(s)
        file.close()

    def print_to_file_nounc(self,filename):

        file = open(filename,'w')
        for i,time in enumerate(self.times):
            #print self.times[i],self.data[i],self.lounc[i],self.hiunc[i]
            s = (str(int(self.times[i]))+',' +
                 str(round(self.data[i],3 )) +'\n' )
            file.write(s)
        file.close()

    def add_year(self,year,data,lounc,hiunc):
        self.times.append(year)
        self.data.append(data)
        self.lounc.append(lounc)
        self.hiunc.append(hiunc)

    def add_name(self,name):
        self.name = name

    def add_offset(self,offset):
        #routine for shifting entire series up or down by a constant offset
        for i in range(0,len(self.times)):
            self.data[i] += offset
            self.lounc[i] += offset
            self.hiunc[i] += offset

    def get_value(self,year):
        return self.data[self.times.index(year)]

    def get_rank_of_year(self,year):
        #this tells you the nominal rank of a particular year 1 is warmest
        years = self.times[:]
        anoms = self.data[:]
        sorted_years = [years for (anoms,years) in sorted(zip(anoms,years))]
        rank = len(self.times)-sorted_years.index(year)
        return rank
    
    def draw_sample(self):
        #assuming that uncertainty ranges is 95% confidence, that the errors
        #have a gaussian distribution and that they are uncorrelated: create
        #a single "realisation" of the data set
        times = self.times[:]
        data = self.data[:]
        lounc = self.lounc[:]
        hiunc = self.hiunc[:]
        for i in range(0,len(times)):
            draw = random.gauss(0,(hiunc[i]-lounc[i])/3.92)
            data[i] += draw
            lounc[i] += draw
            hiunc[i] += draw
        return time_series(times,data,lounc,hiunc)

    def rebaseline(self,year1,year2):
        #change baseline for anomalies
        ind1 = self.times.index(year1)
        ind2 = self.times.index(year2)
        clim = np.mean(self.data[ind1:ind2+1])
        for i in range(0,len(self.data)):
            self.data[i] -= clim
            self.lounc[i] -= clim
            self.hiunc[i] -= clim

    def calculate_average(self,year1,year2):
        ind1 = self.times.index(year1)
        ind2 = self.times.index(year2)
        clim = np.mean(self.data[ind1:ind2+1])
        return clim

    def print_ordered_ts(self,topten):
        #print the warmest n years where n=topten
        print self.name+" Top "+str(topten)
        order = self.data[:]
        order.sort()
        for i in range(len(order)-topten,len(order)):
            print("%3d %4d %7.3f %7.3f %7.3f " % ( len(order)-i,self.times[self.data.index(order[i])], \
                               self.data[self.data.index(order[i])], \
                               self.lounc[self.data.index(order[i])], \
                               self.hiunc[self.data.index(order[i])]))

    def print_ts(self):
        print self.name+" Annual averages"
        print "Year,Anomaly,LowerUncertaintyBound,HigherUncertaintyBound"
        for i in range(0,len(self.data)):
            print("%4d,%7.3f,%7.3f,%7.3f" % (self.times[i],self.data[i],self.lounc[i],self.hiunc[i]))

    def print_period_avg(self,year1,year2):
        #print average of time series from year1 to year2
        index1 = self.times.index(year1)
        index2 = self.times.index(year2)

        print("")
        print "Long Term Averages"
        print ("%4i-%4i avg = %7.3f" % (year1,year2,np.mean(self.data[index1:index2+1])))

    def plot_running_line(self,filter_width,color):
        
        running_mean = []
        running_axis = []

        for i in range(filter_width,len(self.data)):
            running_mean.append(np.mean(self.data[i-filter_width+1:i+1]))
            running_axis.append(np.mean(self.times[i-filter_width+1:i+1]))
#            print (self.times[i-filter_width+1:i+1],
#                   np.mean(self.data[i-filter_width+1:i+1]),
#                   np.mean(self.times[i-filter_width+1:i+1]))
        plt.plot(running_axis,running_mean, linewidth=1.5, color=color, label=self.name)
        
        return running_mean,running_axis

    def plot_running_mean(self,filter_width):

        for w in filter_width:
            n = 1
            while len(self.data)-n*w > w:
                n += 1
            n=n-1
            running_mean = []
            running_axis = []

            plt.plot(running_axis,running_mean, linewidth=0,color='white')

            for i in range(len(self.data)-n*w,len(self.data)+w,w):

                print (str(w)+','+
                       str(self.times[i-w])+','+
                       str(self.times[i-1])+','+
                       str(round(np.mean(self.data[i-w:i]),3)))
                
                running_mean.append(np.mean(self.data[i-w:i]))
                running_axis.append(np.mean(self.times[i-w:i]))

                barthick = 0.5
                l = self.times[i-w]
                r = self.times[i-1]
                d = np.mean(self.data[i-w:i])
                col = 'Coral'
                if d < 0: col = 'DodgerBlue'
                poly = Polygon(zip([l,r,r,l],
                               [0,0,d,d]),facecolor=col,
                               edgecolor="Black",zorder=2,
                               label="GG")
                plt.gca().add_patch(poly)

            
                

        plt.plot([1875,2020],[0,0],color='Black')
        plt.xlabel('Year', fontsize=18)
        plt.ylabel('Anomaly relative to 1961-1990 (K)', fontsize=18)
        plt.axis((1875,2020,-0.62,0.62))
        #plt.axis((1880,2015.5,-0.62,0.62))
        plt.show()
    
    def plot_ts(self, color):
        plt.plot(self.times, self.data, linewidth=1.5, color=color, label=self.name)

    def plot_ts_with_unc(self, colora, colorbk):
        plt.plot(self.times, self.data, linewidth=1.5, color=colora, label=self.name)
        plt.fill_between(self.times, self.lounc, self.hiunc,
                facecolor=colorbk,color=colorbk, alpha=1.00,
                label='1 sigma range')

        mx = max(self.hiunc)
        mn = min(self.lounc)
        delta = 0.1 * (mx-mn)

        plt.axis((1848,2016,mn-delta,mx+delta))

    def plot_skyscraper_diagram(self):

        hfont = {'fontname':'Arial'}
        fsz = 18
        plt.figure(figsize=(16,9))
        
        plt.plot(np.zeros(50), color="White")
#        for i in range(1960,2020,10):
#            plt.plot([i,i],[-10,10],color="DarkGray",zorder=1)

        for i in range(0,len(self.times)):

            y = self.times[i]
            d = self.data[i]

            color = "Beige"

            if nino_year(y) == 0:
                color = "Silver"
            elif nino_year(y) == -1:
                color = "DodgerBlue"
            elif nino_year(y) == 1:
                color = "darkred"

            if y == 2015:
                color = "indianred"

            delta = 0.45
           
            poly = Polygon(zip([y-delta,y+delta,y+delta,y-delta],\
                               [0,0,d,d]),facecolor=color,edgecolor="Black",zorder=2)
            plt.gca().add_patch(poly)

        plt.xlabel('Year', fontdict=hfont, fontsize=fsz)
        plt.ylabel('Anomaly relative to 1981-2010 ($^\circ$C)', fontdict=hfont, fontsize=fsz)

#draw off-screen polygons to get an appropriate legend
        poly = Polygon(zip([0,0,0,0],[0,0,0,0]),facecolor='FireBrick',edgecolor="Black",label="El Nino")
        plt.gca().add_patch(poly)
        poly = Polygon(zip([0,0,0,0],[0,0,0,0]),facecolor='Silver',edgecolor="Black",label="Neutral")
        plt.gca().add_patch(poly)
        poly = Polygon(zip([0,0,0,0],[0,0,0,0]),facecolor='DodgerBlue',edgecolor="Black",label="La Nina")
        plt.gca().add_patch(poly)

        plt.legend(bbox_to_anchor=(0.24, 0.892),
                   bbox_transform=plt.gcf().transFigure, 
                   frameon=False)

        plt.plot([1949.5,2018.5],[0,0],color="Black")
        plt.axis((1949.5,2018.5,-0.72,0.72))
        plt.savefig('Figures/gmt_skyscraper.png', bbox_inches='tight')


def nino_year(year):
    #based on CPC Nino 3.4. Apparently.

    result = 0 #neutral

    elninos = [1958, 1966, 1973, 1983, 1987, 1988, 1998, 2003, 2010, 2015, 2016]
    laninas = [1950, 1955, 1956, 1974, 1976, 1989, 1999, 2000, 2008, 2011]

    if year in laninas:
        result = -1
    elif year in elninos:
        result = 1

    return result
 
