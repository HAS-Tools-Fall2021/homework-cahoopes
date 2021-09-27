# Starter code for homework 5

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt'
filepath = os.path.join('data', filename)
print(os.getcwd())
print(filepath)

filepath = '../data/streamflow_week5.txt'

# %%
# Read the data into a pandas dataframe
data = pd.read_table(filepath, sep = '\t', skiprows=30,
        names =['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] = data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

# %%
# Start by obtaining a basic summary of the dataframe properties
# Also get recent values to use for forecast
print(data.columns)
print(len(data))
print(data.dtypes)
data[["flow"]].describe()
data[["flow"]].tail(10)

# %%
# Split the flow by months and find the statistics for each month
# Was having trouble with groupby, found an alternative method which covered Q5 as well 
# Change the number at the end of the next line to adjust the month
month_data=data[data["month"]==12]
print(month_data[["flow"]].describe())
month_sorted=month_data.sort_values(by='flow')
print(month_sorted.head(1))
print(month_sorted.tail(1))

# %%
# Find the 5 highest and 5 lowest values, along with the date they occured
sorted_data=data.sort_values(by='flow')
print(sorted_data.head())
print(sorted_data.tail())

# Get, print list of historical dates with flow values within 10% of 110 cfs (week 1 forecast)
tenperc=110.0*.1
lowbound=110.0-tenperc
highbound=110.0+tenperc
nearforc=data[(data["flow"]>=lowbound) & (data["flow"]<=highbound)]
forcdates=nearforc["datetime"]

# Too many indices, must write to output file
forcdates.to_csv(index=False)

# %%
