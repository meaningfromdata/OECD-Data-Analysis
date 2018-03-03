# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 07:31:49 2018

@author: David
"""

# Importing the libraries
# Select lines of code with mouse and use fn + f9 to execute
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# endog is dependent var (y)
# exog are independent vars (X)
import statsmodels.api as sm


# list of tuples for cleaning up country names/abbreviations after importing OECD data
oecd_names=[('AUS', 'Australia'),
 ('AUT', 'Austria'),
 ('BEL', 'Belgium'),
 ('BRA', 'Brazil'),
 ('CAN', 'Canada'),
 ('CHE', 'Switzerland'),
 ('CHL', 'Chile'),
 ('COL', 'Colombia'),
 ('CRI', 'Costa Rica'),
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
 ('LTU', 'Lithuania'),
 ('LUX', 'Luxembourg'),
 ('LVA', 'Latvia'),
 ('MEX', 'Mexico'),
 ('NLD', 'Netherlands'),
 ('NOR', 'Norway'),
 ('NZL', 'New Zealand'),
 ('POL', 'Poland'),
 ('PRT', 'Portugal'),
 ('RUS', 'Russia'),
 ('SVK', 'Slovak Republic'),
 ('SVN', 'Slovenia'),
 ('SWE', 'Sweden'),
 ('TUR', 'Turkey'),
 ('USA', 'United States'),
 ('ZAF', 'South Africa')
 ]



# reduced to 34 official OECD countries
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



# read CSV file containing OECD GDP annual growth rate data
gdpGrowthRateData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\\OECD_GDP_annualGrowthRate_1957_2016.csv')

# pare down gdpGrowthRate to only contain three columns:  country, time (year) and value
gdpDF=gdpGrowthRateData[["LOCATION", "TIME", "Value"]]

# rename 'Value' to be 'gdpPct' to be more descriptive and unique after merging
gdpDF.rename(columns = {'Value': 'gdpPct'}, inplace=True)



# read CSV file containing OECD trade union density data 
unionDenData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\OECD_TradeUnionDensity_1960_2014.csv')

# pare down unionDenData to only contain three columns: country, time (year) and value
unionDF=unionDenData[["COUNTRY", "TIME", "Value"]]

# rename 'Value' to be 'unionPct' to be more descriptive and unique after merging
unionDF.rename(columns = {'COUNTRY':'LOCATION', 'Value': 'unionDensityPct'}, inplace=True)



# read CSV file containing OECD Gini coefficient data
giniData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\OECD_giniCoeff_2011incomeMethod_1974_2013.csv')

# pare down giniData to only contain three columns: country, time (year) and value
giniDF=giniData[["LOCATION", "Year", "Value"]]

# rename 'Value' to be 'gini' to be more descriptive and unique after merging
giniDF.rename(columns = {'Year':'TIME', 'Value': 'gini'}, inplace=True)



# read CSV file containing OECD hours worked data
hoursWorkedData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\OECD_hoursWorkedPerWorker_perYear_1950_2016.csv')

# pare down hoursWorkedData to only contain three columns:  country, time (year) and value
hoursWorkedDF=hoursWorkedData[["LOCATION", "TIME", "Value"]]

# rename 'Value' to be 'hoursWorked' to be more descriptive and unique after merging
hoursWorkedDF.rename(columns = {'Value': 'hoursWorked'}, inplace=True)



# load data on foreign born (immigrants) as percent of population
foreignBornPctData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\OECD_foreignBorn_pctOfPopulation_1981_2013.csv')

# pare down foreignBornPctData to only contain three columns:  country, time (year) and value
foreignBornPctDF= foreignBornPctData[['LOCATION','TIME','Value']]

# rename 'Value' to be 'foreignBornPct' to be more descriptive and unique after merging
foreignBornPctDF.rename(columns = {'Value': 'foreignBornPct'}, inplace=True)



# load data on working age population as percent of population
workingAgePctData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\OECD_workingAgePopulation_pctOfPopulation_1950_2016.csv')

# pare down workingAgePctData to only contain three columns:  location, time (year) and value
workingAgePctDF= workingAgePctData[['LOCATION','TIME','Value']]

# rename 'Value' to be 'workingAgePct' to be more descriptive and unique after merging
workingAgePctDF.rename(columns = {'Value': 'workingAgePct'}, inplace=True)



# load data on labor force participation as percent of population
laborPartPctData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\OECD_laborForceParticipation_percentOf15to65YearOlds_1960_2010.csv')

# pare down workingAgePctData to only contain three columns:  location, time (year) and value
laborPartPctDF= laborPartPctData[['LOCATION','TIME','Value']]

# rename 'Value' to be 'laborPartPct' to be more descriptive and unique after merging
laborPartPctDF.rename(columns = {'Value': 'laborPartPct'}, inplace=True)



# load data on annual population growth rate
popGrowthPctData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\OECD_population_annualGrowthRate_1950_2014.csv')

# pare down workingAgePctData to only contain three columns:  location, time (year) and value
popGrowthPctDF= popGrowthPctData[['LOCATION','TIME','Value']]

# rename 'Value' to be 'popGrowthPct' to be more descriptive and unique after merging
popGrowthPctDF.rename(columns = {'Value': 'popGrowthPct'}, inplace=True)



# load data on total tax revenue as percent of GDP
totalTaxRevData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\OECD_totalTaxRevenue_pctOfGDP_1965_2015.csv')

#  pare down totalTaxRevData to only contain three columns: country, time (year) and value
totalTaxRevDF= totalTaxRevData[['LOCATION','TIME','Value']]

# rename 'Value' to be 'taxRevPct' to be more descriptive and unique after merging
totalTaxRevDF.rename(columns = {'Value': 'taxRevPct'}, inplace=True)



# load data on annual government deficit as percent of GDP
govDeficitData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\OECD_genGovtDeficit_pctOfGDP_1970_2016.csv')

#  pare down govDeficitData to only contain three columns: country, time (year) and value
govDeficitDF= govDeficitData[['LOCATION','TIME','Value']]

# rename 'Value' to be 'govDefPct' to be more descriptive and unique after merging
govDeficitDF.rename(columns = {'Value': 'govDefPct'}, inplace=True)



# load data on annual government spending as percent of GDP
govSpendingDF=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\OECD_genSpending_pctOfGDP_1970_2016.csv')

#  pare down govDeficitData to only contain three columns: country, time (year) and value
govSpendingDF= govSpendingDF[['LOCATION','TIME','Value']]

# rename 'Value' to be 'govSpendingPct' to be more descriptive and unique after merging
govSpendingDF.rename(columns = {'Value': 'govSpendingPct'}, inplace=True)



# load data on household spending as percent of gdp
householdSpendingPctData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\OECD_householdSpending_pctGDP_1960_2016.csv')

#  pare down govDeficitData to only contain three columns: location (country), time (year) and value
hholdSpendingPctDF= householdSpendingPctData[['LOCATION','TIME','Value']]

# rename 'Value' to be 'householdSpendPct' to be more descriptive and unique after merging
hholdSpendingPctDF.rename(columns = {'Value': 'hholdSpendPct'}, inplace=True)



# load data on savings as percent of gdp
savingRateData=pd.read_csv('C:\\Users\\David\\Documents\\Data Science Related\\Datasets\\OECD_Stats\OECD_savingRate_pctOfGDP_1970_2016.csv')

#  pare down savingRateData to only contain three columns: location (country), time (year) and value
savingRateDF= savingRateData[['LOCATION','TIME','Value']]

# rename 'Value' to be 'savingPct' to be more descriptive and unique after merging
savingRateDF.rename(columns = {'Value': 'savingPct'}, inplace=True)




# create list of the dataframes to be merged with gdpDF  
merge_list = [unionDF, giniDF, hoursWorkedDF, foreignBornPctDF, workingAgePctDF, popGrowthPctDF, totalTaxRevDF, govDeficitDF, govSpendingDF, laborPartPctDF, hholdSpendingPctDF, savingRateDF]


# initialize gdpDF_merged dataframe that will be used for merging with dataframes containing predictors in for loop below
gdpDF_merged = gdpDF

# INNER JOIN (INTERSECTION) VS OUTER JOIN (UNION) MERGING 
# with how='outer' for union of two dfs at each merge step
for df in merge_list:
    gdpDF_merged = pd.merge(left=gdpDF_merged, right=df, how='outer', on=['LOCATION','TIME'])
    

# reduce dataset to only OECD members (34 countries)
gdpDF_oecdOnly = gdpDF_merged[gdpDF_merged['LOCATION'].isin(oecd_names_1D)]    
    


# plot scatterplots with regression line of all columns against gdp annual growth rate (gdpPct)
for i in range(2, len(gdpDF_oecdOnly.columns)):
    plt.figure(i)
    sns.regplot(gdpDF_oecdOnly.columns[i], gdpDF_oecdOnly.gdpPct, data=gdpDF_oecdOnly)



# calculate the correlation matrix (correlations among columns of matrix)
corr = gdpDF_oecdOnly.dropna().corr()

# plot a heatmap of the correlation matrix
sns.heatmap(corr, 
        xticklabels=corr.columns,
        yticklabels=corr.columns)



# NEEDS SOME OUTLIER ANALYSIS FOR SOME OF THESE FEATURES 

# DO I NEED TO USE BONFERRONI CORRECTION WHEN DOING THESE?
#  AM I DOING MULTIPLE COMPARISONS EVEN WHEN FITTING OLS?  


# first just doing ordinary least squares for gdpPct vs all columns individually
for columnNum in range(3, len(gdpDF_oecdOnly.columns)):
    X = gdpDF_oecdOnly.dropna().iloc[:,columnNum] ## X usually means our input variables (or independent variables)
    y = gdpDF_oecdOnly.dropna()["gdpPct"] ## Y usually means our output/dependent variable
    X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model
    # Note the difference in argument order
    model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
    predictions = model.predict(X)
    # Print out the statistics
    print(model.summary())
    # four newlines to space out print-out summary 
    print('\n' * 4)
   
    
# MAYBE EXTRACT ALL SIGNIFICANT PREDICTORS, THEIR 95% CI AND THEIR R-SQUARED
    
    
    
# THEN DO A "KITCHEN SINK" MULTIPLE REGRESSION
    
    
    