#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install pandas')


# In[3]:


import csv
import pandas as pd
from tensorflow import keras


# In[4]:


columns_of_interest = ['start_time', 'end_time']
columns_of_interest.extend(['start_station_id', 'start_station_name'])
columns_of_interest.extend(['start_station_latitude', 'start_station_longitude'])
columns_of_interest.extend(['end_station_id', 'end_station_name'])
columns_of_interest.extend(['end_station_latitude', 'end_station_longitude'])
columns_of_interest


# In[5]:


'''bike201700 = pd.DataFrame(pd.read_csv('2017-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201801 = pd.DataFrame(pd.read_csv('201801-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201802 = pd.DataFrame(pd.read_csv('201802-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201803 = pd.DataFrame(pd.read_csv('201803-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201804 = pd.DataFrame(pd.read_csv('201804-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201805 = pd.DataFrame(pd.read_csv('201805-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201806 = pd.DataFrame(pd.read_csv('201806-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201807 = pd.DataFrame(pd.read_csv('201807-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201808 = pd.DataFrame(pd.read_csv('201808-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201809 = pd.DataFrame(pd.read_csv('201809-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201810 = pd.DataFrame(pd.read_csv('201810-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201811 = pd.DataFrame(pd.read_csv('201811-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201812 = pd.DataFrame(pd.read_csv('201812-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201901 = pd.DataFrame(pd.read_csv('201901-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201902 = pd.DataFrame(pd.read_csv('201902-fordgobike-tripdata.csv'), columns=columns_of_interest)
bike201903 = pd.DataFrame(pd.read_csv('201903-fordgobike-tripdata.csv'), columns=columns_of_interest)'''


# In[6]:


'''rowtotal = bike201700.shape[0] + bike201801.shape[0] + bike201802.shape[0] + bike201803.shape[0]
rowtotal = rowtotal + bike201804.shape[0] + bike201805.shape[0] + bike201806.shape[0] + bike201807.shape[0]
rowtotal = rowtotal + bike201808.shape[0] + bike201809.shape[0] + bike201810.shape[0] + bike201811.shape[0]
rowtotal = rowtotal + bike201812.shape[0] + bike201901.shape[0] + bike201902.shape[0] + bike201903.shape[0]
rowtotal'''


# In[7]:


'''allbikedata = pd.concat([bike201700, bike201801, bike201802, bike201803, bike201804, bike201805, bike201806])
allbikedata = pd.concat([allbikedata, bike201807, bike201808, bike201809, bike201810, bike201811, bike201812])
allbikedata = pd.concat([allbikedata, bike201901, bike201902, bike201903])'''


# In[8]:


#allbikedata.to_csv('allbikedata.csv')
allbikedata = pd.DataFrame(pd.read_csv('allbikedata.csv'), columns=columns_of_interest)


# In[174]:


startstations = allbikedata["start_station_name"].tolist()
endstations = allbikedata["end_station_name"].tolist()
allstations = set(startstations + endstations)

allstations


# In[10]:


# Label Station locations by city
# San Francisco: 37.7749° N, 122.4194° W
# San Jose: 37.3382° N, 121.8863° W
# East Bay:
#     Oakland: 37.8044° N, 122.2711° W
#     Berkeley: 37.8716° N, 122.2727° W
#     Emeryville: 37.8313° N, 122.2852° W

startlat = allbikedata['start_station_latitude'].tolist()
endlat = allbikedata['end_station_latitude'].tolist()

startlon = allbikedata['start_station_longitude'].tolist()
endlon = allbikedata['end_station_longitude'].tolist()


alllat = set(startlat + endlat)
alllon = set(startlon + endlon)


# In[11]:


# About 5 hours to preprocess data (and remove non-SF station information) and construct the basic model pipeline


# In[12]:


allbikedata['start_city'] = ['San Francisco' if -1*int(100*x) >= 12235 else 'Other' for x in allbikedata['start_station_longitude']]
allbikedata['end_city'] = ['San Francisco' if -1*int(100*x) >= 12235 else 'Other' for x in allbikedata['end_station_longitude']]


# In[13]:


intercity = allbikedata[allbikedata['start_city'] != allbikedata['end_city']]
#intercity


# In[14]:


# Collect list of all SF Stations

sfstarts = allbikedata[allbikedata['start_city'] == 'San Francisco']
sfends = allbikedata[allbikedata['end_city'] == 'San Francisco']

sfstations = set(sfstarts["start_station_name"].tolist() + sfends["end_station_name"].tolist())

sfstations


# In[15]:


# List of all SF trips (nonintercity)

sftrips = pd.concat([sfstarts, sfends])
sftrips = sftrips[sftrips['start_city'] == sftrips['end_city']]
sftrips


# In[16]:


# Use station list: sfstations
# Also add intercity stats
# TAKES > 5 minutes

totalvisits = {}
for idx, row in sftrips.iterrows():
    currentstart = row['start_station_name']
    currentend = row['end_station_name']

    if currentstart in sfstations:
        if currentstart in totalvisits:
            totalvisits[currentstart] += 1
        else:
            totalvisits[currentstart] = 1

    if currentend in sfstations:
        if currentend in totalvisits:
            totalvisits[currentend] += 1
        else:
            totalvisits[currentend] = 1

for idx, row in intercity.iterrows():
    currentstart = row['start_station_name']
    currentend = row['end_station_name']

    if currentstart in sfstations:
        if currentstart in totalvisits:
            totalvisits[currentstart] += 1
        else:
            totalvisits[currentstart] = 1

    if currentend in sfstations:
        if currentend in totalvisits:
            totalvisits[currentend] += 1
        else:
            totalvisits[currentend] = 1
totalvisits


# In[17]:


#import json
#with open('total_visits.json', 'w') as fp:
#    json.dump(totalvisits, fp)


# In[18]:


### BASE DATASET FOR DAILY PREDICTION DATA
from datetime import datetime

sftrips['start_weekday'] = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f').weekday() for x in sftrips['start_time']]
sftrips['end_weekday'] = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f').weekday() for x in sftrips['end_time']]
sftrips['start_month'] = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f').month for x in sftrips['start_time']]
sftrips['end_month'] = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f').month for x in sftrips['end_time']]
sftrips['start_day'] = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f').day for x in sftrips['start_time']]
sftrips['end_day'] = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f').day for x in sftrips['end_time']]
sftrips['start_year'] = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f').year for x in sftrips['start_time']]
sftrips['end_year'] = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f').year for x in sftrips['end_time']]
sftrips['start_hour'] = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f').hour for x in sftrips['start_time']]
sftrips['end_hour'] = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f').hour for x in sftrips['end_time']]
sftrips


# In[21]:


# Create a dataframe with the following column labels: Station Name, Weekday, Hour (24h), Date(M/D/Y), Numvisits

# To send for training: Station Name, Weekday, Hour, Numvisits

# Inputs: Station Name, Hour, Weekday
# Output: Numvisits

# Dictionary to calculate Usage totals
# Key: "Year-Month-Day,Hour,Weekday,Station Name"
# Value: int(Numvisits)
hourly_station_usage = {}

for idx, row in sftrips.iterrows():

    startdate = str(row['start_year']) + '-' + str(row['start_month']) + '-' + str(row['start_day'])
    enddate = str(row['end_year']) + '-' + str(row['end_month']) + '-' + str(row['end_day'])

    key1 = str(startdate)+','+str(row['start_hour'])+','+str(row['start_weekday'])+','+str(row['start_station_name'])
    key2 = str(enddate)+','+str(row['end_hour'])+','+str(row['end_weekday'])+','+str(row['end_station_name'])

    if key1 in hourly_station_usage:
        hourly_station_usage[key1] += 1
    else:
        hourly_station_usage[key1] = 1
    if key2 in hourly_station_usage:
        hourly_station_usage[key2] += 1
    else:
        hourly_station_usage[key2] = 1

hourly_station_usage


# In[22]:


# Be sure to state that the intercity trips were not included (191 --> verify this number)


# In[23]:


#import json
#with open('hourly_station_usage.json', 'w') as fp:
#    json.dump(hourly_station_usage, fp)


# In[33]:


import json
with open('hourly_station_usage.json', 'r') as fp:
    data = fp.read()
hourlyvisits = json.loads(data)

hourly_reshaped = []
columns = ['date', 'hour', 'weekday', 'station_name', 'num_visits']

for key in hourlyvisits:
    [date, hr, wd, sn] = key.split(',')
    nv = hourlyvisits[key]

    hourly_reshaped.append([date, int(hr), int(wd), sn, nv])

df_hourly_visits = pd.DataFrame(hourly_reshaped, columns=columns)
df_hourly_visits


# In[ ]:





# In[44]:


#df_hourly_visits.to_csv('hourly_visits_by_station_daily.csv')


# In[ ]:
