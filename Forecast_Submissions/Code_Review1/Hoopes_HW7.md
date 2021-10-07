Homework 7 submission - by Andrew Hoopes

Python script instructions
In addition to downloading the most recent streamflow, there are a couple of variables which must be set in order for the script to run properly.  The variable date on line 118 must be set to 11, the 11th of October being the day when the forecast period starts.  On the line above, the variable precip should be set according to the level of precipitation expected during week 1 of the forecast period.  Using the NWS forecast accesible via https://forecast.weather.gov/MapClick.php?lon=-111.85758589999749&lat=34.56146253137916#.YV4DsCVlDYs, add up all the precip probabilities for each day (do not combine day and night probabilities, if both are greater than 0, use the greater of the two) and divide by 50%, rounding down to the nearest integer.  Example: 3 days of 30% would give a precip value of 1, adding a 10% day would increase the value to 2.  If no probability is given for a day, assume its value is 0.

Week 1 forecast:
Week 2: Forecast:

Printed script outputs:

Saved figures:

Code review:
