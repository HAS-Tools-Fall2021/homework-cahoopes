# Starter code for Homework 4

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week4.txt'
filepath = os.path.join('../data', filename)
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

# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%
# Starter Code:
# Start making your changes here. 

#NOTE: You will be working with the numpy array 'flow_data'
# Flow data has a row for every day and 4 columns:
# 1. Year
# 2. Month
# 3. Day of the month
# 4. Flow value in CFS

# _______________
# Example 1: counting the number of values with flow > 600 and month ==7
# Note we are doing this by asking for the rows where the flow column (i.e. Flow_data[:,3]) is >600
# And where the month column (i.e. flow_data[:,1]) is equal to 7

# 1a. Here is how to do that on one line of code
flow_count = np.sum((flow_data[:,3] > 600) & (flow_data[:,1]==7))
print(flow_count)

# Here is the same thing broken out into multiple lines:
flow_test = flow_data[:, 3] > 600  # Note that this returns a 1-d array that has an entry for every day of the timeseies (i.e. row) with either a true or a fals
month_test = flow_data[:, 1] ==7   # doing the same thing but testing if month =7 
combined_test = flow_test & month_test  # now looking at our last two tests and finding when they are both true
flow_count = np.sum(combined_test) # add up all the array (note Trues = 1 and False =0) so by default this counts all the times our criteria are true
print(flow_count)

#__________________________
## Example 2: Calculate the average flow for these same criteria 
# 2.a How to do it with one line of code: 
# Note this is exactly like the line above exexpt now we are grabbing out the flow data
# and then taking the averge
flow_mean = np.mean(flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7),3])

# 2.b The same thing split out into multiple steps
criteria = (flow_data[:, 3] > 600) & (flow_data[:, 1] == 7)  # This returns an array of true fals values with an entrry for every day, telling us where our criteria are met
flow_pick = flow_data[criteria, 3] #Grab out the 4th column (i.e. flow) for every row wherer the criteria was true
flow_mean =  np.mean(flow_pick) # take the average of the values you extracted

print("Flow meets this critera", flow_count, " times")
print('And has an average value of', np.round(flow_mean,2), "when this is true")

#__________________________
## Example 3: Make a histogram of data

# step 1: Use the linspace  funciton to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=15)
# another example using the max flow to set the upper limit for the bins
#mybins = np.linspace(0, np.max(flow_data[:,3]), num=15) 

#Step 2: plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

#__________________________
## Example 4: Get the quantiles of flow

# 4.a  Apply the np.quantile function to the flow column 
# grab out the 10th, 50th and 90th percentile flow values
flow_quants1 = np.quantile(flow_data[:,3], q=[0,0.1, 0.5, 0.9])
print('Method one flow quantiles:', flow_quants1)

# 4.b  use the axis=0 argument to indicate that you would like the funciton 
# applied along columns. In this case you will get quantlies for every column of the 
# data automatically 
flow_quants2 = np.quantile(flow_data, q=[0,0.1, 0.5, 0.9], axis=0)
#note flow_quants2 has 4 columns just like our data so we need to say flow_quants2[:,3]
# to extract the flow quantiles for our flow data. 
print('Method two flow quantiles:', flow_quants2[:,3]) 
