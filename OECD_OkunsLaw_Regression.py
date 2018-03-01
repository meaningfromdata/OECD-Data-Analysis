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




# import datasets

# read CSV file containing OECD GDP annual growth rate data
gdpGrowthRateData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\\OECD_GDP_annualGrowthRate_1957_2016.csv')

# pare down gdpGrowthRate to only contain three columns:  country, time (year) and value
gdpDF=gdpGrowthRateData[["LOCATION", "TIME", "Value"]]

# rename 'Value' to be 'gdpPct' to be more descriptive and unique after merging
gdpDF.rename(columns = {'Value': 'gdpPct'}, inplace=True)



# read CSV file containing OECD GDP annual growth rate data
harmUnEmpData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\\OECD_harmonizedUnemploymentRate_pctOfLabourForce_1955_2016.csv')

# pare down gdpGrowthRate to only contain three columns:  country, time (year) and value
harmUnEmpDataDF=harmUnEmpData[["LOCATION", "TIME", "Value"]]

# rename 'Value' to be 'gdpPct' to be more descriptive and unique after merging
harmUnEmpDataDF.rename(columns = {'Value': 'unEmpPct'}, inplace=True)






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


# intersection (inner join) of gdp and harmonized unemployment rate datasets 
gdpAndUnempDF = pd.merge(left=gdpDF, right=harmUnEmpDataDF, how='inner', on=['LOCATION','TIME'])
    

# reduce dataset to only OECD members (34 countries)
gdpAndUnempDF_oecdOnly = gdpAndUnempDF[gdpAndUnempDF['LOCATION'].isin(oecd_names_1D)]    













# minimum number of observations required to select country for regression
minObservations = 30

# CONSIDER ALSO MAKING YEARS OF OBSERVATIONS SAME FOR ALL COUNTRIES

# initialize dictionary to store results of interest in
country_results = {}


# regress year-to-year gdp growth rate against unemployment rate using statsmodels  
# print summary of model
# plot regression with seaborn
for country in sorted(list(set(gdpAndUnempDF_oecdOnly['LOCATION']))):
    countryTemp_df = gdpAndUnempDF_oecdOnly.loc[gdpAndUnempDF_oecdOnly['LOCATION']==country].dropna()
    if countryTemp_df.shape[0]>=minObservations:
        X = countryTemp_df['unEmpPct'] ## X usually means our input variables (or independent variables)
        y = countryTemp_df['gdpPct'] ## Y usually means our output/dependent variable
        X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model
        # Note the difference in argument order
        model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
        predictions = model.predict(X)
        # Print out the statistics
        print(str(country))
        print(model.summary())
        plt.figure(country)
        sns.regplot(countryTemp_df['unEmpPct'], countryTemp_df['gdpPct'], data=countryTemp_df)
        # four newlines to space out print-out summary 
        print('\n' * 4)
    


# plot distributions of residuals 

for country in sorted(list(set(gdpAndUnempDF_oecdOnly['LOCATION']))):
    countryTemp_df = gdpAndUnempDF_oecdOnly.loc[gdpAndUnempDF_oecdOnly['LOCATION']==country].dropna()
    if countryTemp_df.shape[0]>=minObservations:
        X = countryTemp_df['unEmpPct'] ## X usually means our input variables (or independent variables)
        y = countryTemp_df['gdpPct'] ## Y usually means our output/dependent variable
        X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model
        # Note the difference in argument order
        model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
        predictions = model.predict(X)
        # Print out the statistics
        # print(str(country))
        # print(model.summary())
        plt.figure(country)
        sns.distplot(model.resid_pearson)
        # four newlines to space out print-out summary 
        print('\n' * 4)
