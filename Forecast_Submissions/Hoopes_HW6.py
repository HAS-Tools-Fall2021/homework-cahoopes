# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week6.txt'
filepath = os.path.join('../data/', filename)
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
plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots()
ax.plot(data['datetime'], data['flow'], color='steelblue', label='last month')
ax.set(title="Observed Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        xlim=[datetime.date(2021, 9, 1), datetime.date(2021, 9, 30)],
        ylim=[0, 250])
ax.legend()
plt.show()
fig.savefig("Observed_Flow.png")

# %%
# Plot the October flows for the last 10 years
fig, ax = plt.subplots()
colorlist=['green','steelblue','crimson','gold','slategray','navy','lime','yellow',
    'silver','peru','magenta']
colpick=0
for i in range(2010, 2021):
#        colpick=i
        plot_data=data[(data['year']==i) & (data['month']==10)]
        ax.plot(plot_data['day'], plot_data['flow'], color=colorlist[i-2010],
                label=i)
ax.legend()
fig.savefig("Last_10_Octobers.png")

# %%
# scatterplot this years flow vs last years flow for september
# years are 2020, 2021
fig, ax = plt.subplots()
ax.scatter(data[(data['year'] == 2020) & (data['month'] == 9)].flow,  data[(data['year'] == 2021) & (data['month'] == 9)].flow, marker='p',
           color='crimson')
ax.set(xlabel='2019 flow', ylabel='2020 flow')
fig.savefig("2_year_comparison.png")

# %%
# Scatter plot of flow vs day of the month for October
# Dots are colored by the year and sized acccording to the flow
oct_data = data[data['month']==10] #grabbing just October flows for plotting
fig, ax = plt.subplots()
ax.scatter(oct_data['day'], oct_data['flow'], alpha=0.7,
            s=0.02*oct_data['flow'], c=oct_data['year'], cmap='viridis')
ax.set_xlabel('Day of the month')
ax.set_ylabel('Flow')
plt.show()
fig.savefig("Weighted_Scatter.png")

# %%
# Figure out how the flow behaves in October
# - find the mean flow for each day of the month
plt.style.use('seaborn-whitegrid')
oct_mean=oct_data.groupby('day')['flow'].mean()
fig, ax = plt.subplots()
ax.plot(oct_mean.index, oct_mean.values, color='crimson', label='October mean')
ax.set(title="Mean October Flow", xlabel="Day of Month", ylabel="October Mean Flow [cfs]")
ax.legend()
plt.show()
fig.savefig("October_mean.png")

# %%
# Multipanel plot histograms of flow for September and October
my_bins=np.linspace(0,800,num=30)
fig, ax = plt.subplots(1,2)

m = 9
month_data = data[data['month'] == m]
plot_title = 'Month ' + str(m)
ax[0].hist(month_data['flow'], bins=my_bins, 
        edgecolor='lightgrey', color='gold')
ax[0].set(xlabel='September Flow cfs', ylabel='count', title=plot_title)

m=10
month_data = data[data['month'] == m]
plot_title = 'Month ' + str(m)
ax[1].hist(month_data['flow'], bins=my_bins,
           edgecolor='lightgrey', color='gold')
ax[1].set(xlabel='October Flow cfs', ylabel='count', title= plot_title)
plt.show()
fig.savefig("Double_histogram.png")
# %%
