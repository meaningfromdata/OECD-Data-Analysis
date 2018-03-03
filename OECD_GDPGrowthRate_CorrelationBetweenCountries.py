# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 18:06:04 2018

@author: David
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 12:00:33 2018

@author: David
"""


# Importing the libraries

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm

from scipy.cluster.hierarchy import dendrogram, linkage



# import datasets

# read CSV file containing OECD GDP annual growth rate data
gdpGrowthRateData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\\OECD_GDP_annualGrowthRate_1957_2016.csv')

# pare down gdpGrowthRate to only contain three columns:  country, time (year) and value
gdpDF=gdpGrowthRateData[["LOCATION", "TIME", "Value"]]

# rename 'Value' to be 'gdpPct' to be more descriptive and unique after merging
gdpDF.rename(columns = {'Value': 'gdpPct'}, inplace=True)




"""

# read CSV file containing OECD GDP annual growth rate data
harmUnEmpData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\\OECD_harmonizedUnemploymentRate_pctOfLabourForce_1955_2016.csv')

# pare down gdpGrowthRate to only contain three columns:  country, time (year) and value
harmUnEmpDataDF=harmUnEmpData[["LOCATION", "TIME", "Value"]]

# rename 'Value' to be 'gdpPct' to be more descriptive and unique after merging
harmUnEmpDataDF.rename(columns = {'Value': 'unEmpPct'}, inplace=True)

"""






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
yearsToCover = list(np.arange(1975,2015,1))


gdpDF_yearsToCover = pd.DataFrame(index=yearsToCover) 



# separate data frame by country and check that the range of years of interest
# is contained in this country's data frame
for country in sorted(list(set(gdpDF_oecdOnly['LOCATION']))):
    countryTemp_df = gdpDF_oecdOnly.loc[gdpDF_oecdOnly['LOCATION']==country].dropna()
    temp_Bools = list(countryTemp_df['TIME'].isin(yearsToCover))
    if len(yearsToCover) == temp_Bools.count(True):
        countryTemp_df = countryTemp_df.loc[(countryTemp_df['TIME']>= yearsToCover[0]) & (countryTemp_df['TIME']<= yearsToCover[-1])]
        gdpDF_yearsToCover[country] = countryTemp_df['gdpPct'].values



# generate heatmap of correlations between gdpPct of all OECD countries with 
# at least 40 years of data
sns.heatmap(gdpDF_yearsToCover.corr(), annot=True, fmt=".2f")


# IS THIS CLUSTERING THE COLUMNS OR THE ROWS???
# hierarchical clustering of correlation matrix
Z = linkage(gdpDF_yearsToCover, 'single', 'correlation')
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
    #labels=gdpDF_yearsToCover.columns
)
plt.show()




# also possible to visualize clustering in seaborn
# sns.clustermap(gdpDF_yearsToCover, metric="correlation")


    
# gdpDF_yearsToCover_forPlotting = gdpDF_yearsToCover.melt(gdpDF_yearsToCover.index, var_name='cols', value_name='vals')        





    
# sns.factorplot(x="index", y="vals", hue='cols', data=gdpDF_yearsToCover_forPlotting)

