# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
# import datetime

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
# Temporarily set up with old data, will update when it is time to make new forecast
filename = 'streamflow_week6.txt'
filepath = os.path.join('../../data', filename)
print(os.getcwd())
print(filepath)

# %%
#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code'],
        parse_dates=['datetime']
        )

# Expand the dates to year month day
data['year'] = pd.DatetimeIndex(data['datetime']).year
data['month'] = pd.DatetimeIndex(data['datetime']).month
data['day'] = pd.DatetimeIndex(data['datetime']).day
data['dayofweek'] = pd.DatetimeIndex(data['datetime']).dayofweek

# %%
# Time series of flow values with the x axis range limited
# Adjust this plot, make it look at the most recent month
recent_data=data.tail(30)
plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots()
ax.plot(recent_data['datetime'], recent_data['flow'], color='steelblue', label='Last Month')
ax.set(title="Observed Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]")
ax.legend()
plt.show()
# fig.savefig('Recent_flow_updated.png')

# %%
# Histogram plot of October flow
oct_data = data[data['month']==10]
my_bins=np.linspace(0,800,num=30)
fig, ax = plt.subplots()
plot_title = 'October Streamflow Histogram'
ax.hist(oct_data['flow'], bins=my_bins,
           edgecolor='lightgrey', color='gold')
ax.set(xlabel='October Flow cfs', ylabel='count', title= plot_title)
plt.show()
# fig.savefig('October_histogram.png')

# %%
# Figure out how the flow behaves in October
# - find the mean flow for each day of the month
oct_mean=oct_data.groupby('day')['flow'].mean()
fig, ax = plt.subplots()
ax.plot(oct_mean.index, oct_mean.values, color='crimson', label='October mean')
ax.set(title="Mean October Flow", xlabel="Day of Month", ylabel="October Mean Flow [cfs]")
ax.legend()
plt.show()
# fig.savefig('October_mean.png')

# %%
# Also consider median flow
oct_median=oct_data.groupby('day')['flow'].median()
fig, ax = plt.subplots()
ax.plot(oct_median.index, oct_median.values, color='crimson', label='October median')
ax.set(title="Median October Flow", xlabel="Day of Month", ylabel="October Median Flow [cfs]")
ax.legend()
plt.show()
# fig.savefig('October_median.png')

# %%
# Create and run a function which forecasts the streamflow for the next two weeks based on 
# current flow and monthly climatology (mean and median flows)
# For week 1, also include whether significant precip is expected, set based on number of days where
# chance of precipitation is >=50% (NWS forecast)
# Link : https://forecast.weather.gov/MapClick.php?lon=-111.85758589999749&lat=34.56146253137916#.YV4DsCVlDYs
# Cumulative, so 2 days with 30% chance equal one day of 50% chance
# Day, night probabilities separate, use whichever value is higher to represnt the day
# Example: for 3 30% days, set precip index to 1.  A 4th day would increase the index to 2
# Do not include for week 2, too far out to reliably predict significant events
# Instead, weight climatology higher for second week, as opposed to equal weights of first week
# Note: equal weight means mean and median combined are equal to last observation

def flowcast(obs,mean,med,a,day):
    """ This function takes the last streamflow observation and interpolates streamflow for the next two weeks
    using the climatological mean and median flow to weight the interpolation.
    For the first week, additional weighting comes from precipitation, while climatology is weighted higher 
    during the second week. 
    Inputs: obs - last streamflow observation in the initial PANDAS Dataframe
    mean - mean flow for the month of the forecast (October)
    med: - median flow for the month of the forecast (October)
    a - number of days where precipitation is expected, set based on combined NWS daily precipitation
    probabilities divided by 50
    day - day of the month of the Monday at the start of the forecast period
    Outputs: 2 forecast values (f1 and f2), f1 for the first week, and f2 for the second week"""
    
    week1=np.zeros(7)
    week2=np.zeros(7)
    for i in range(7):
        week1[i]=mean.values[day+i]*0.25+med.values[day+i]*0.25+obs*0.5
        week2[i]=mean.values[day+i+7]*0.4+med.values[day+i+7]*0.4+obs*0.2
    f1=round(np.mean(week1)*(1+(a-1)/10))
    f2=round(np.mean(week2))
    return(f1,f2)

# Define the necessary variables and call the function
# Manually set precipitation index using link, explanation above
# Set date based on day of month of first day in week 1 forecast period
# Should be set to 11 for week 7.
last_flow=recent_data["flow"].iloc[-1]
precip=1
date=3
flowcast1,flowcast2=flowcast(last_flow,oct_mean,oct_median,precip,date)
print('Week 1 forecast:',flowcast1,'cfs')
print('Week 2 forecast:',flowcast2,'cfs')

# %%
