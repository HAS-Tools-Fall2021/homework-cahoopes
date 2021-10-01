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
filename = 'streamflow_week2.txt'
filepath = os.path.join('../data', filename)
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
fig.set_size_inches(5,3)
fig.savefig("Observed_Flow.png")


#2. Time series of flow values with the x axis range limited
fig, ax = plt.subplots()
ax.plot(data['datetime'], data['flow'], label='full')
ax.set(title="Observed Flow", xlabel="Date", ylabel="Weekly Avg Flow [cfs]",
        yscale='log', xlim=[datetime.date(2000, 1, 26), datetime.date(2014, 2, 1)])
ax.legend()
plt.show()


#3 Boxplot of flows by month 
fig, ax = plt.subplots()
ax = sns.boxplot(x="month", y="flow",  data=data,
                 linewidth=0.3)
ax.set(yscale='log')
# Here i'm separating out the x lable and ylable setting just as an illustration
# They also could have been included in the ax.set command above
ax.set_xlabel('Forecast Week')
ax.set_ylabel('Flow (cfs)')
plt.show()


# 4. Plot the september flows for the last 10 years
fig, ax = plt.subplots()
for i in range(2010, 2022):
        plot_data=data[(data['year']==i)] # and data['month']==9)]
        ax.plot(plot_data['datetime'], plot_data['flow'], color='green',
                linestyle='dashed', label='daily')

#5. scatterplot this years flow vs last years flow for september
fig, ax = plt.subplots()

ax.scatter(data[(data['year'] == 2019) & (data['month'] == 9)].flow,  data[(data['year'] == 2020) & (data['month'] == 9)].flow, marker='p',
           color='blueviolet')
ax.set(xlabel='2019 flow', ylabel='2020 flow', yscale='log', xscale='log')
ax.legend()

# 6. Scatter plot of flow vs day of the month for september
# Dots are colored by the year and sized acccording to the flow
sept_data = data[data['month']==9] #grabbing just september flows for plotting
fig, ax = plt.subplots()
ax.scatter(sept_data['day'], sept_data['flow'], alpha=0.2,
            s=0.02*sept_data['flow'], c=sept_data['year'], cmap='viridis')
ax.set(yscale='log')
ax.set_xlabel('Day of the month')
ax.set_ylabel('Flow')
plt.show()

#7. Multipanel plot histograms of flow for September and October
fig, ax = plt.subplots(1,2)

m = 9
month_data = data[data['month'] == m]
plot_title = 'Month ' + str(m)
ax[0].hist(np.log10(month_data['flow']), bins=30, edgecolor='grey', color='steelblue')
ax[0].set(xlabel='Log Flow cfs', ylabel='count', title=plot_title)

m=10
month_data = data[data['month'] == m]
plot_title = 'Month ' + str(m)
ax[1].hist(np.log10(month_data['flow']), bins=30,
           edgecolor='grey', color='steelblue')
ax[1].set(xlabel='Log Flow cfs', ylabel='count', title= plot_title)
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
