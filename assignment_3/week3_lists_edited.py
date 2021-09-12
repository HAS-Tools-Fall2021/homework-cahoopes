# Start code for assignment 3
# this code sets up the lists you will need for your homework
# and provides some examples of operations that will be helpful to you

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week3.txt'
filepath = os.path.join('/home/hoopescandrew/HAS_Tools', filename)
print(os.getcwd())
print(filepath)

# %%
# DON'T change this part -- this creates the lists you
# should use for the rest of the assignment
# no need to worry about how this is being done now we will cover
# this in later sections.

#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

#make lists of the data
flow = data.flow.values.tolist()
date = data.datetime.values.tolist()
year = data.year.values.tolist()
month = data.month.values.tolist()
day = data.day.values.tolist()

# Getting rid of the pandas dataframe since we wont be using it this week
# del(data)
# Could not make a graph without the dataframe, needed it to view flow

# %%
# Here is some starter code to illustrate some things you might like to do
# Modify this however you would like to do your homework.
# From here on out you should use only the lists created in the last block:
# flow, date, yaer, month and day

# Calculating some basic properites
print(min(flow))
print(max(flow))
print(np.mean(flow))
print(np.std(flow))
print(type(day))
print(type(day[0]))
print(len(day))

# Making and empty list that I will use to store
# index values I'm interested in
ilist = []
ilist2 = []

# Loop over the length of the flow list
# and adding the index value to the ilist
# if it meets some criteria that I specify
for i in range(len(flow)):
        if year[i] >= 2010 and month[i] == 9:
                ilist.append(i)
        if year[i] >= 2010 and flow [i] > 75 and month [i] == 9:
                ilist2.append(i)

# Loop for Q4 - compare first and last halves of September
ilist3 = []
ilist4 = []
for k in range(len(flow)):
        if month[k] == 9 and day[k] <= 15:
                ilist3.append(k)
        if month [k] == 9 and day[k] >= 16:
                ilist4.append(k)

# see how many times the criteria was met by checking the length
# of the index list that was generated, compare with base list
print(len(ilist))
print(len(ilist2))
flow_frac=len(ilist2)/len(ilist)
print(flow_frac)

# Grabbing out the data that met the criteria
# This  subset of data is just the elements identified
# in the ilist
# Display the basic statistics of this data (September flow)
subset3 = [flow[j] for j in ilist3]
subset4 = [flow[l] for l in ilist4]
print(min(subset3))
print(max(subset3))
print(np.mean(subset3))
print(np.std(subset3))
print(min(subset4))
print(max(subset4))
print(np.mean(subset4))
print(np.std(subset4))

# Alternatively I could have  written the for loop I used
# above to  create ilist like this
# ilist2 = [i for i in range(len(flow)) if flow[i] > 600 and month[i]==7]
# print(len(ilist2))

# Now make a plot of the data
ax=data.iloc[11925:11941]['flow'].plot(linewidth=0.5)
ax.set_ylabel('Daily Flow [cfs]')
ax.set_xlabel('Date')

# %%
