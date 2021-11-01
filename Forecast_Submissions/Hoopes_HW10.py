# %%
# Import the modules we will use
# import os
import numpy as np
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter as df
from matplotlib.dates import DayLocator as dl
import json
import urllib.request as req
import urllib
# import datetime

# %%
# Get data from online, read into pandas dataframe
flow_url = "https://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb" \
           "&site_no=09506000&referred_module=sw" \
           "&period=&begin_date=1989-01-01&end_date=2021-10-30"
flow_data = pd.read_table(flow_url, sep='\t', skiprows=30,
                          names=['agency_cd', 'site_no', 'datetime', 'flow',
                                 'code'], parse_dates=['datetime'])

# Expand the dates to year month day, set index as base datetime
flow_data['year'] = pd.DatetimeIndex(flow_data['datetime']).year
flow_data['month'] = pd.DatetimeIndex(flow_data['datetime']).month
flow_data['day'] = pd.DatetimeIndex(flow_data['datetime']).day
flow_data['dayofweek'] = pd.DatetimeIndex(flow_data['datetime']).dayofweek
flow_data = flow_data.set_index('datetime')

# %%
# Obtain climatological precipitation data from multiple sources in forecast
# region, use this to aid in deduction of precipitation influence on
# climatological streamflow
# First source - Prescott, Arizona - Data from 2000-10-27 to present
# Data from mesonet site

# First insert token, create the URL for the rest API
mytoken = '2434260f200d4f929e79fe8418777acb'
base_url = "http://api.mesowest.net/v2/stations/timeseries"

# Specific arguments for Prescott
args = {
    'start': '199701010000',
    'end': '202012310000',
    'obtimezone': 'UTC',
    'vars': 'precip_accum_24_hour',
    'stids': 'KPRC',
    'units': 'precip|mm',
    'token': mytoken}

# Take arguments and paste them together into a string for the api
apiString = urllib.parse.urlencode(args)
print(apiString)

# add the API string to the base_url
fullUrl = base_url + '?' + apiString
print(fullUrl)

# Request and read the data
response = req.urlopen(fullUrl)
responseDict = json.loads(response.read())
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
precip = responseDict['STATION'][0]['OBSERVATIONS']['precip_accum_24_hour_set_1']

# Now we can combine this into a pandas dataframe
precip_data = pd.DataFrame({'Precipitation (mm)': precip},
                           index=pd.to_datetime(dateTime))

# Now convert this to daily data using resample
# Data has nan values for all non-2f-hour interval timestamps, must remove
psr_daily = precip_data.resample('D').max()
psr_daily['Precipitation (mm)'] = psr_daily['Precipitation (mm)'].fillna(0)
psr_daily['year'] = pd.DatetimeIndex(psr_daily.index).year
psr_daily['month'] = pd.DatetimeIndex(psr_daily.index).month
psr_daily['day'] = pd.DatetimeIndex(psr_daily.index).day

# %%
# Second source - Flagstaff, Arizona - Data from 2000-10-28 to present
# Data from mesonet site

# Specific arguments for Flagstaff
args = {
    'start': '199701010000',
    'end': '202012310000',
    'obtimezone': 'UTC',
    'vars': 'precip_accum_24_hour',
    'stids': 'KFLG',
    'units': 'precip|mm',
    'token': mytoken}

# Take arguments and paste them together into a string for the api
apiString = urllib.parse.urlencode(args)
print(apiString)

# add the API string to the base_url
fullUrl = base_url + '?' + apiString
print(fullUrl)

# Request and read the data
response = req.urlopen(fullUrl)
responseDict = json.loads(response.read())
dateTime = responseDict['STATION'][0]['OBSERVATIONS']['date_time']
precip = responseDict['STATION'][0]['OBSERVATIONS']['precip_accum_24_hour_set_1']

# Now we can combine this into a pandas dataframe
precip_data = pd.DataFrame({'Precipitation (mm)': precip},
                           index=pd.to_datetime(dateTime))

# Now convert this to daily data using resample
# Data has nan values for all non-2f-hour interval timestamps, must remove
fgz_daily = precip_data.resample('D').max()
fgz_daily['Precipitation (mm)'] = fgz_daily['Precipitation (mm)'].fillna(0)
fgz_daily['year'] = pd.DatetimeIndex(fgz_daily.index).year
fgz_daily['month'] = pd.DatetimeIndex(fgz_daily.index).month
fgz_daily['day'] = pd.DatetimeIndex(fgz_daily.index).day

# %%
# Third source  - Daymet data from Camp Verde Area, csv format
# Data availiable from 1989 to the end of 2020
url = "https://daymet.ornl.gov/single-pixel/api/data?lat=34.5582" \
       "&lon=-111.8591&vars=prcp&start=1989-01-01&end=2020-12-31" \
       "&format=csv"
csv_data = pd.read_table(url, delimiter=',', skiprows=6)

# %%
# Time series of flow values with the x axis range limited
# Adjust this plot, make it look at the most recent month
# New for week 8 - clean up datetime format on x-axis
recent_flow = flow_data.tail(30)
xformat = df("%m-%d")
plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots()
ax.plot(recent_flow['flow'], color='steelblue', label='Last Month')
ax.xaxis.set_major_formatter(xformat)
ax.xaxis.set_major_locator(dl(interval=4))
ax.set(title="Observed Flow", xlabel="Date (Year is 2021)",
       ylabel="Weekly Avg Flow [cfs]")
ax.legend()
plt.show()
# fig.savefig('Recent_flow_week9.png')

# %%
# Figure out how the flow behaves in forecast month(s)
# - find the mean flow for each day of the month
nov_data = flow_data[flow_data['month'] == 11]
nov_mean = nov_data.groupby('day')['flow'].mean()
fig, ax = plt.subplots()
ax.plot(nov_mean.index, nov_mean.values, color='crimson',
        label='November mean')
ax.set(title="Mean Monthly Flow", xlabel="Day of Month",
       ylabel="Mean Monthly Flow [cfs]")
ax.legend()
plt.show()
# fig.savefig('Monthly_mean.png')

# %%
# Also consider median flow
nov_median = nov_data.groupby('day')['flow'].median()
fig, ax = plt.subplots()
ax.plot(nov_median.index, nov_median.values, color='crimson',
        label='November median')
ax.set(title="Median Monthly Flow", xlabel="Day of Month",
       ylabel=" Median Monthly Flow [cfs]")
ax.legend()
plt.show()
# fig.savefig('Monthly_median.png')

# %%
# Now organize and plot precip values from 3 outside sources
# Use similar method as flow data for mesonet data
# csv data in yday format, must be organized differently
# Only need to worry about first forecast week here
# Use means to make plot of cumulative precipitation
# expected over the month of interest
# Do not use median, few enough events that all days are zero

nov_psr = psr_daily[psr_daily['month'] == 11]
psr_mean = nov_psr.groupby('day')['Precipitation (mm)'].mean()
nov_fgz = fgz_daily[fgz_daily['month'] == 11]
fgz_mean = nov_fgz.groupby('day')['Precipitation (mm)'].mean()
nov_cvd = csv_data[csv_data['yday'] >= 305]
nov_cvd = nov_cvd[nov_cvd['yday'] <= 334]
cvd_mean = nov_cvd.groupby('yday')['prcp (mm/day)'].mean()
psr_climo = psr_mean.cumsum()
fgz_climo = fgz_mean.cumsum()
cvd_climo = cvd_mean.cumsum()

fig, ax = plt.subplots()
ax.plot(psr_mean.index, psr_climo, color='steelblue',
        label='Prescott')
ax.plot(fgz_mean.index, fgz_climo, color='crimson',
        label='Flagstaff')
ax.plot(fgz_mean.index, cvd_climo, color='gold',
        label='Camp Verde')
ax.set(title="Mean Monthly Precipitation", xlabel="Day of Month",
       ylabel="Cumulative Precipitation Totals (mm)")
ax.legend()
plt.show()
# fig.savefig('Mean_precip_cumulative.png')

# %%
# Also figure out likelihood of precipitation on any given day of the month,
# use to generate number of days precip can be expected in first week
psr_bool = (nov_psr['Precipitation (mm)'] > 0).astype(int)
fgz_bool = (nov_fgz['Precipitation (mm)'] > 0).astype(int)
cvd_bool = (nov_cvd['prcp (mm/day)'] > 0).astype(int)
psr_prob = psr_bool.values.sum()/psr_bool.size
print(psr_prob)
fgz_prob = fgz_bool.values.sum()/fgz_bool.size
print(fgz_prob)
cvd_prob = cvd_bool.values.sum()/cvd_bool.size
print(cvd_prob)
total_prob = round((psr_prob+fgz_prob+cvd_prob)/3.0, 2)
print(total_prob)

# %%
# Create and run a function which forecasts the streamflow for the next two
# weeks based on current flow and monthly climatology (mean and median flows)
#
# For week 1, also include whether significant precip is expected, set based
# on number of days where chance of precipitation is >=50% (NWS forecast)

# Link: https://forecast.weather.gov/MapClick.php?lon=-111.85758589999749&lat=34.56146253137916#.YV4DsCVlDYs

# Cumulative, so 2 days with 30% chance equal one day of 50% chance

# Day, night probabilities separate,
# use whichever value is higher to represent the day

# Example: for 3 30% days, set precip index to 1
# A 4th day would increase the index to 2


# New for week 9 - add climatological component - based on 11% chance of precip
# per day in month of November, 11%*7=77%, 1 day of precip expected per week

# Do not include for week 2, too far out to reliably predict significant events

# Instead, weight climatology higher for second week,
# as opposed to equal weights of first week

# Equal weight means mean and median combined are equal to last observation


def flowcast(obs, mean, med, a, b, day):
    """ A fuction to interpolate streamflow using observations and climatology.

    This function takes the last streamflow observation and interpolates
    streamflow for the next two weeks using the climatological
    mean and median flow to weight the interpolation.  For the first week,
    additional weighting comes from precipitation,
    while climatology is weighted higher during the second week.

    Inputs: obs (float) - last streamflow observation in the initial
    PANDAS Dataframe, extracted from dataframe as a float value
    mean (pandas series) - mean flow for the month of the forecast (October)
    med (pandas series) - median flow for the month of the forecast (October)
    If forecast period includes multiple months add second mean, med input
    a (int) - number of days where precipitation is expected,
    set based on combined NWS daily precipitation probabilities divided by 50
    b (int) - number of days when precipitation is expected based on local
    climatology at 3 locations, base probability per day calculated earlier
    day (int) - day of the month of Sunday before the forecast period's start

    Outputs: 2 forecast values (f1 and f2),
    f1 for the first week, and f2 for the second week"""

    week1 = np.zeros(7)
    week2 = np.zeros(7)
    for i in range(7):
        week1[i] = mean.values[day+i]*0.25+med.values[day+i]*0.25+obs*0.5
        week2[i] = mean.values[day+i+7]*0.4+med.values[day+i+7]*0.4+obs*0.2
    f1 = round(np.mean(week1)*(1+(a-b)/10))
    f2 = round(np.mean(week2))
    return(f1, f2)


# Define the necessary variables and call the function

# Manually set precipitation index using link, explanation above

# Set date based on day of month of day before first day
# in week 1 forecast period
# Climatological index for November of 1 day per week
# No precip expected this week
# Day should be set to 0 (Oct 31) for week 10.

last_flow = recent_flow["flow"].iloc[-1]
precip = 0
climo = 1
date = 0
flowcast1, flowcast2 = flowcast(last_flow, nov_mean, nov_median, precip,
                                climo, date)
print('Week 1 forecast:', flowcast1, 'cfs')
print('Week 2 forecast:', flowcast2, 'cfs')

# %%
