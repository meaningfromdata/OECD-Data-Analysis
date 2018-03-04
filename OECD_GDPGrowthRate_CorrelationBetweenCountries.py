# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 18:06:04 2018

@author: David

Correlating and Clustering GDP Perecent Growth Timeseries for those OECD Countries 
With Data from 1975-2015

"""



# Importing the libraries

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
# import statsmodels.api as sm

from scipy.cluster.hierarchy import dendrogram, linkage


# import datasets

# read CSV file containing OECD GDP annual growth rate data
gdpGrowthRateData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\\OECD_GDP_annualGrowthRate_1957_2016.csv')

# pare down gdpGrowthRate to only contain three columns:  country, time (year) and value
gdpDF=gdpGrowthRateData[["LOCATION", "TIME", "Value"]]

# rename 'Value' to be 'gdpPct' to be more descriptive and unique after merging
gdpDF.rename(columns = {'Value': 'gdpPct'}, inplace=True)








# abbreviation and names of 34 official OECD countries
oecd_member_names=[('AUS', 'Australia'),
 ('AUT', 'Austria'),
 ('BEL', 'Belgium'),
 ('CAN', 'Canada'),
 ('CHE', 'Switzerland'),
 ('CHL', 'Chile'),
 ('CZE', 'Czech Republic'),
 ('DEU', 'Germany'),
 ('DNK', 'Denmark'),
 ('ESP', 'Spain'),
 ('EST', 'Estonia'),
 ('FIN', 'Finland'),
 ('FRA', 'France'),
 ('GBR', 'United Kingdom'),
 ('GRC', 'Greece'),
 ('HUN', 'Hungary'),
 ('IRL', 'Ireland'),
 ('ISL', 'Iceland'),
 ('ISR', 'Israel'),
 ('ITA', 'Italy'),
 ('JPN', 'Japan'),
 ('KOR', 'Korea'),
 ('LUX', 'Luxembourg'),
 ('MEX', 'Mexico'),
 ('NLD', 'Netherlands'),
 ('NOR', 'Norway'),
 ('NZL', 'New Zealand'),
 ('POL', 'Poland'),
 ('PRT', 'Portugal'),
 ('SVK', 'Slovak Republic'),
 ('SVN', 'Slovenia'),
 ('SWE', 'Sweden'),
 ('TUR', 'Turkey'),
 ('USA', 'United States'),
 ]


# extract first column from oecd_member_names as list
oecd_names_1D = [name[0] for name in oecd_member_names]


# reduce dataset to only OECD members (34 countries)
gdpDF_oecdOnly = gdpDF[gdpDF['LOCATION'].isin(oecd_names_1D)]    





# years of interest for correlating gdp growth rate (gdpPct)
yearsToCover = list(np.arange(1975,2016,1))


gdpDF_yearsToCover = pd.DataFrame(index=yearsToCover) 



# separate data frame by country and then check that the range of years of interest
# is contained in this country's data frame
for country in sorted(list(set(gdpDF_oecdOnly['LOCATION']))):
    countryTemp_df = gdpDF_oecdOnly.loc[gdpDF_oecdOnly['LOCATION']==country].dropna()
    temp_Bools = list(countryTemp_df['TIME'].isin(yearsToCover))
    if len(yearsToCover) == temp_Bools.count(True):
        countryTemp_df = countryTemp_df.loc[(countryTemp_df['TIME']>= yearsToCover[0]) & (countryTemp_df['TIME']<= yearsToCover[-1])]
        gdpDF_yearsToCover[country] = countryTemp_df['gdpPct'].values



# plot GDP Percent Growth Rate (year-over-year) timeseries for all countries 
plot = gdpDF_yearsToCover.plot(x=gdpDF_yearsToCover.index, y=gdpDF_yearsToCover.columns, title='GDP Growth Rate for OECD Members from 1975-2015')

plot.set_xlabel("Year")
plot.set_ylabel("GDP Percent Growth Rate")
plt.show()



# copy gdpDF_yearsToCover into new data frame that columns with stats will be appended to
gdpDF_yearsToCoverWithStats = gdpDF_yearsToCover.copy()

# calculate mean and standard deviation for each row (each timepoint)
gdpDF_yearsToCoverWithStats['mean']= gdpDF_yearsToCover.mean(axis=1)
gdpDF_yearsToCoverWithStats['sd']= gdpDF_yearsToCover.std(axis=1)
gdpDF_yearsToCoverWithStats['mean+sd'] = gdpDF_yearsToCoverWithStats['mean'] + gdpDF_yearsToCoverWithStats['sd']
gdpDF_yearsToCoverWithStats['mean-sd'] = gdpDF_yearsToCoverWithStats['mean'] - gdpDF_yearsToCoverWithStats['sd']


# plot mean +/- sd of GDP Percent Growth Rate (year-over-year) timeseries for all countries 
# plot2 = gdpDF_yearsToCoverWithStats.plot(x=gdpDF_yearsToCoverWithStats.index, y=['mean', 'mean+sd', 'mean-sd'], title='Mean +/- SD of GDP Growth Rate for OECD Members from 1975-2015',  style=['-','--','--'], color=['k', 'k', 'k'], linewidth=1.5)

# plot2.set_xlabel("Year")
# plot2.set_ylabel("GDP Percent Growth Rate")
# plt.show()



# plot sd of GDP Percent Growth Rate (year-over-year) timeseries for all countries 
# plot3 = gdpDF_yearsToCoverWithStats.plot(x=gdpDF_yearsToCoverWithStats.index, y='sd', title='Standard Deviation of GDP Growth Rate for OECD Members from 1975-2015')

# plot3.set_xlabel("Year")
# plot3.set_ylabel("GDP Percent Growth Rate")
# plt.show()





# overlaying plots of GDP Percent Growth Rate (year-over-year) timeseries for all countries and mean +/- standard deviation
ax = gdpDF_yearsToCover.plot(x=gdpDF_yearsToCover.index, y=gdpDF_yearsToCover.columns, title='GDP Growth Rate for OECD Members from 1975-2015')
_ = gdpDF_yearsToCoverWithStats.plot(x=gdpDF_yearsToCoverWithStats.index, y=['mean', 'mean+sd', 'mean-sd'], style=['-','--','--'], color=['k', 'k', 'k'], linewidth=2.0, ax=ax)

ax.set_xlabel("Year")
ax.set_ylabel("GDP Percent Growth Rate")
plt.show()



# generate heatmap of correlations between gdpPct of all OECD countries with 
# at least 40 years of data
sns.heatmap(gdpDF_yearsToCover.corr(), annot=True, fmt=".2f")




# hierarchical clustering of correlation matrix
Z = linkage(gdpDF_yearsToCover.corr(), 'single')
plt.title('Dendrogram of GDP Growth Rate (1975-2015)')
plt.xlabel('Country')
plt.ylabel('distance')
dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
    labels=list(gdpDF_yearsToCover.columns)
)
plt.show()



