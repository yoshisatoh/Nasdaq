#################### Nasdaq Data Link : Get raw data ####################
#
#  (C) 2021, Yoshimasa (Yoshi) Satoh, CFA 
#
#  All rights reserved.
#
# Created:      2021/10/18
# Last Updated: 2021/10/18
#
# Github:
# https://github.com/yoshisatoh/Nasdaq/tree/main/data/raw/Nominal_GDP_per_capita/nasdaq.data.raw.py
#
#
########## Input Data Files
#
# You have to create a text file (api_key.txt) with only one line of Quandl's API key in it, and then save it on the same direcoty with this script (nasdaq.data.raw.py)
# api_key.txt
#
# Also, generate csv data (e.g., codes.csv) for Nasdaq Data Link / Quandl codes to load.
#
#
########## Usage Instructions
#
# Run this py script on Terminal of MacOS (or Command Prompt on Windows) as follows:
# python nasdaq.data.raw.py codes.csv
#
# python nasdaq.data.raw.py (csv file for Nasdaq Data Link / Quandl codes to load)
#
#
########## Output Data Files
#
# df2.csv
# All the results to draw a graph
#
#
########## References
#
#Quandl on GitHub:
#https://github.com/quandl/quandl-python
#
#Nasdaq Data Link (formerly known as Quandl)
#https://data.nasdaq.com/search
#
#Gross Domestic Product Per Capita for Australia
#https://data.nasdaq.com/data/FRED/PCAGDPAUA646NWDB-gross-domestic-product-per-capita-for-australia
#
#Gross Domestic Product Per Capita for Canada
#https://data.nasdaq.com/data/FRED/PCAGDPCAA646NWDB-gross-domestic-product-per-capita-for-canada
#
#Gross Domestic Product Per Capita for Japan
#https://data.nasdaq.com/data/FRED/PCAGDPJPA646NWDB-gross-domestic-product-per-capita-for-japan
#
#Gross Domestic Product Per Capita for Sweden
#https://data.nasdaq.com/data/FRED/PCAGDPSEA646NWDB-gross-domestic-product-per-capita-for-sweden
#
#Gross Domestic Product Per Capita for United Kingdom
#https://data.nasdaq.com/data/FRED/PCAGDPGBA646NWDB-gross-domestic-product-per-capita-for-united-kingdom
#
#Gross Domestic Product Per Capita for United States
#https://data.nasdaq.com/data/FRED/PCAGDPUSA646NWDB-gross-domestic-product-per-capita-for-united-states
#
#
####################################################################################################




########## install Python libraries
#
# pip on your Terminal on MacOS (or Command Prompt on Windows) might not work.
#pip install quandl
#
# If that's the case, then try:
#pip install --upgrade quandl --trusted-host pypi.org --trusted-host files.pythonhosted.org
#
# If it's successful, then you can repeat the same command for other libraries (i.e., numpy, pandas, and matplotlib.pyplot).
#
#




########## import Python libraries
#
import sys

from csv import reader

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quandl




########## arguments
for i in range(len(sys.argv)):
    print(str(sys.argv[i]))

codes_file = str(sys.argv[1])




########## Nasdaq Data Link / Quandl api_key
#
#
##### Read Quandle api_key from api_key.txt
with open('api_key.txt','r') as f:
    api_key = f.read()
    #
    #read() – read all text from a file into a string. This method is useful if you have a small file and you want to manipulate the whole text of that file.
    #readline() – read the text file line by line and return all the lines as strings.
    #readlines() – read all the lines of the text file and return them as a list of strings.
    #
    #print(api_key)
#
#f.close()
#print(f.closed)
print(api_key)
#
#
##### Set Quandle api_key
quandl.ApiConfig.api_key = api_key




########## Nasdaq Data Link / Quandl security Code
#
#
##### Read Quandl security codes as a list.

with open(codes_file, 'r') as codes_file:
    csv_reader = reader(codes_file)
    # Passing the csv_reader object to list() to get a list of lists
    list_codes = list(csv_reader)
    print(list_codes)

'''
FRED/PCAGDPAUA646NWDB,Australia
FRED/PCAGDPCAA646NWDB,Canada
FRED/PCAGDPJPA646NWDB,Japan
FRED/PCAGDPSEA646NWDB,Sweden
FRED/PCAGDPGBA646NWDB,United Kingdom
FRED/PCAGDPUSA646NWDB,United States
'''




########## Get raw data from Quandl and draw a graph

#print(len(list_codes))    #6

plt.figure(1, figsize=(16, 8))


for i in range(len(list_codes)):
    #
    ##### Raw Data
    #
    code = list_codes[i][0]
    df = quandl.get(code)
    #
    #print(df.head())
    '''
                      Value
    Date
    1960-01-01  1807.785710
    1961-01-01  1874.732106
    1962-01-01  1851.841851
    1963-01-01  1964.150470
    1964-01-01  2128.068355
    '''
    #print(df.index)
    #
    #print(df.index.name)    #Date
    #
    #print(df.columns)    #Index(['Value'], dtype='object')
    #
    #print(df['Value'].head())
    '''
    Date
    1960-01-01    1807.785710
    1961-01-01    1874.732106
    1962-01-01    1851.841851
    1963-01-01    1964.150470
    1964-01-01    2128.068355
    Name: Value, dtype: float64
    '''
    #
    #
    ##### Draw a graph
    #df.plot(figsize=(16, 8))
    #
    #print(list_codes[i][1])
    #print(type(list_codes[i][1]))
    plt.plot(df.index, df['Value'], label=list_codes[i][1])
    #plt.plot(df.index, df['Value'], label='label')
    #
    #
    ##### rename y-axis data to individual country name
    df = df.rename(columns={'Value': list_codes[i][1]})
    #
    #
    ##### Merging individual df into df2 for all results
    if i == 0:
        df2 = df
    else:
        df2 = pd.merge(df2, df, left_index=True, right_index=True)


#plt.legend(loc="upper left", ncol=len(df.columns))
plt.legend(loc="upper left", ncol=len(list_codes))

#plt.xlabel(df.index.name)
plt.xlabel('Date')
plt.ylabel('Nominal GDP per capita in USD')

plt.savefig("df2.png")
df2.to_csv('df2.csv', sep=',', header=True, index=True)

plt.show()

plt.close("all")


