# Starter code for week 6 illustrating how to build an AR model 
# and plot it

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
#note you may need to do pip install for sklearn

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week5.txt'
filepath = os.path.join('/home/hoopescandrew/HAS_Tools/', filename)
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
# Here are some examples of things you might want to plot to get you started:

# 1. Timeseries of observed weekly flow values
fig, ax = plt.subplots()
ax.plot(data['datetime'], data['flow'], color='green',
        linestyle='dashed', label='daily')
ax.set(title="Observed Flow", xlabel="Date", 
        ylabel="Daily Avg Flow [cfs]",
        yscale='log')
ax.legend()
# an example of saving your figure to a file
# fig.set_size_inches(5,3)
# fig.savefig("Observed_Flow.png")


#2. Time series of flow values with the x axis range limited
# Adjust this plot, make it look at the most recent month
plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots()
ax.plot(data['datetime'], data['flow'], color='steelblue', label='last month')
ax.set(title="Observed Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        xlim=[datetime.date(2021, 9, 1), datetime.date(2021, 9, 24)],
        ylim=[0, 250])
ax.legend()
plt.show()

# %%
#3 Boxplot of flows by month 
plt.style.use('default')
fig, ax = plt.subplots()
ax = sns.boxplot(x="month", y="flow",  data=data,
                 linewidth=0.3)
ax.set(yscale='log')
# Here i'm separating out the x lable and ylable setting just as an illustration
# They also could have been included in the ax.set command above
ax.set_xlabel('Forecast Week')
ax.set_ylabel('Flow (cfs)')
plt.show()


# 4. Plot the October flows for the last 10 years
fig, ax = plt.subplots()
for i in range(2010, 2022):
        plot_data=data[(data['year']==i)] # and data['month']==10)]
        ax.plot(plot_data['datetime'], plot_data['flow'], color='green',
                linestyle='dashed', label='daily')

#%%
#5. scatterplot this years flow vs last years flow for september
# Change years to 2020, 2021
fig, ax = plt.subplots()

ax.scatter(data[(data['year'] == 2019) & (data['month'] == 9)].flow,  data[(data['year'] == 2020) & (data['month'] == 9)].flow, marker='p',
           color='blueviolet')
ax.set(xlabel='2019 flow', ylabel='2020 flow')
ax.legend()

# %%
# 6. Scatter plot of flow vs day of the month for september
# Change month to October
# Dots are colored by the year and sized acccording to the flow
oct_data = data[data['month']==10] #grabbing just september flows for plotting
fig, ax = plt.subplots()
ax.scatter(oct_data['day'], oct_data['flow'], alpha=0.7,
            s=0.02*oct_data['flow'], c=oct_data['year'], cmap='viridis')
ax.set_xlabel('Day of the month')
ax.set_ylabel('Flow')
plt.show()

# Figure out how the flow behaves in October
# - find the mean flow for each day of the month
plt.style.use('seaborn-whitegrid')
oct_mean=oct_data.groupby('day')['flow'].mean()
fig, ax = plt.subplots()
ax.plot(oct_mean.iloc[:,0], oct_mean.iloc[:,1], color='crimson', label='October mean')
ax.set(title="Mean October Flow", xlabel="Day of Month", ylabel="October Mean Flow [cfs]")
ax.legend()
plt.show()

# %%
#7. Multipanel plot histograms of flow for September and October
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

#8. Same as 7 but using a for loop to do all 12 months
fig, ax = plt.subplots(2, 2)
ax= ax.flatten()  #so that we can refer to plots as ax[0]...ax[3] rather than ax[0,0]..ax[1,1]
axi = 0
for m in range(9,13):
        month_data = data[data['month'] == 1]
        plot_title = 'Month ' + str(m)
        ax[axi].hist(np.log10(month_data['flow']), bins=30,
           edgecolor='grey', color='steelblue')
        ax[axi].set(xlabel='Log Flow cfs', ylabel='count', title=plot_title)
        axi=axi+1
plt.show()


#Figure out how to do multi conditionals

# %%
