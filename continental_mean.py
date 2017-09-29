import read_data_sets as rd
import matplotlib.pyplot as plt

for country in ["africa","asia","europe","northAmerica","oceania","southAmerica"]:

    ts = rd.read_noaa_continents(country)
    ts.rebaseline(1981,2010)

    ts.plot_ts('red')
    plt.show()

