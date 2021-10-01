#################### Nasdaq Data Link : Get raw data ####################
#
#  (C) 2021, Yoshimasa (Yoshi) Satoh, CFA 
#
#  All rights reserved.
#
# Created:      2021/10/01
# Last Updated: 2021/10/01
#
# Github:
# https://github.com/yoshisatoh/Nasdaq/tree/main/data/raw/nasdaq.data.raw.py
#
#
########## Input Data Files
#
# You have to create a text file (api_key.txt) with only one line of Quandl's API key in it, and then save it on the same direcoty with this script (nasdaq.data.raw.py)
# api_key.txt
#
# You do not need other input files as this program gets data from Nasdaq via the Internet by using the Quandl API key above.
#
#
########## Usage Instructions
#
# Run this py script on Terminal of MacOS (or Command Prompt on Windows) as follows:
# python nasdaq.data.raw.py (Nasdaq Data Link Code) (columns to show)
#
# For instance,
# python nasdaq.data.raw.py USTREASURY/YIELD all
# python nasdaq.data.raw.py USTREASURY/YIELD "10 YR"
# python nasdaq.data.raw.py USTREASURY/YIELD "1 YR" "10 YR"
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
#US Treasury
#https://data.nasdaq.com/data/USTREASURY-us-treasury
#
#Treasury Yield Curve Rates
#https://data.nasdaq.com/data/USTREASURY/YIELD-treasury-yield-curve-rates
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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quandl




########## arguments
for i in range(len(sys.argv)):
    print(str(sys.argv[i]))




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
f.close()
#print(f.closed)
print(api_key)
#
#
##### Set Quandle api_key
quandl.ApiConfig.api_key = api_key




########## Nasdaq Data Link / Quandl security Code
#
#
##### Read Quandl security code from a first argument
code = str(sys.argv[1])
#print(type(code))
#print(code)




########## Get raw data from Quandl
df = quandl.get(code)




########## View Quandl data
#
#print(type(df))
#<class 'pandas.core.frame.DataFrame'>
#
#print(df.index)
'''
DatetimeIndex(['1990-01-02', '1990-01-03', '1990-01-04', '1990-01-05',
               '1990-01-08', '1990-01-09', '1990-01-10', '1990-01-11',
               '1990-01-12', '1990-01-16',
               ...
               '2021-09-17', '2021-09-20', '2021-09-21', '2021-09-22',
               '2021-09-23', '2021-09-24', '2021-09-27', '2021-09-28',
               '2021-09-29', '2021-09-30'],
              dtype='datetime64[ns]', name='Date', length=7946, freq=None)
'''
#
#print(df.columns)
'''
Index(['1 MO', '2 MO', '3 MO', '6 MO', '1 YR', '2 YR', '3 YR', '5 YR', '7 YR',
       '10 YR', '20 YR', '30 YR'],
      dtype='object')
'''
#
df.to_csv('df.csv', sep=',', header=True, index=True)




########## Draw a graph

#print(type(df.index))
#<class 'pandas.core.indexes.datetimes.DatetimeIndex'>

#print(df['10 YR'])
#print(type(df['10 YR']))
#<class 'pandas.core.series.Series'>


if str(sys.argv[2]) == "all":
    #
    #[Option A] All columns
    #
    df.plot(figsize=(16, 8))
    #plt.figure(figsize=(16,8))
    #
    #print(len(df.columns))
    plt.legend(loc="upper right", ncol=len(df.columns))
    #
    #
else:
    #
    #[Option B] Selected column(s)
    #
    plt.figure(figsize=(16,8))
    #
    #print(len(sys.argv))
    #
    for i in range(2, len(sys.argv)):
        #print(str(sys.argv[i]))
        plt.plot(df.index.values, df[str(sys.argv[i])], label=str(sys.argv[i]))
    #
    plt.legend(loc="upper right", ncol=(len(sys.argv)-2))
    #
    #
#
#print(df.index)
#print(df.index.name)
#
#plt.xlabel("Date")
plt.xlabel(df.index.name)
#
'''
print(df.max(axis='index'))
print(type(df.max(axis='index')))
print(df.max(axis='index').max(axis='index'))
print(round(df.max(axis='index').max(axis='index'),0))
print(df.min(axis='index'))
print(type(df.min(axis='index')))
print(df.min(axis='index').min(axis='index'))
print(round(df.min(axis='index').min(axis='index'), 0))
'''
plt.ylim([round(df.min(axis='index').min(axis='index'), 0)-1, round(df.max(axis='index').max(axis='index'),0)+1])
#
#plt.ylabel("Yield")
plt.ylabel(str(sys.argv[1]))
#
plt.savefig("df.png")
#
plt.show()
#
plt.close("all")
