#################### Nasdaq Data Link : Get currency exchange rate data and calculate daily & cumulative USD returns ####################
#
#  (C) 2021, Yoshimasa (Yoshi) Satoh, CFA 
#
#  All rights reserved.
#
# Created:      2021/10/05
# Last Updated: 2021/10/05
#
# Github:
# https://github.com/yoshisatoh/Nasdaq/tree/main/data/returns/equity/nasdaq.data.returns.equity.py
#
#
########## Input Data Files
#
# You have to create a text file (api_key.txt) with only one line of Quandl's API key in it, and then save it on the same direcoty with this script (data.nasdaq.currency.returns.py)
#api_key.txt
#
# You do not need other input files as this program gets data from Nasdaq via the Internet by using the Quandl API key above.
#
#
########## Usage Instructions
#
#Run this py script on Windows Command Prompt as follows:
#python nasdaq.data.returns.equity.py
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
#NASDAQ OMX Global Index Data
#https://data.nasdaq.com/data/NASDAQOMX-nasdaq-omx-global-index-data
#
#NASDAQ Composite (COMP)
#https://data.nasdaq.com/data/NASDAQOMX/COMP-nasdaq-composite-comp
#
#NASDAQ Composite Total Return (XCMP)
#https://data.nasdaq.com/data/NASDAQOMX/XCMP-nasdaq-composite-total-return-xcmp
#
#NASDAQ-100 (NDX)
#https://data.nasdaq.com/data/NASDAQOMX/NDX-nasdaq100-ndx
#
#NASDAQ-100 Total Return (XNDX)
#https://data.nasdaq.com/data/NASDAQOMX/XNDX-nasdaq100-total-return-xndx
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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quandl




########## arguments
for i in range(len(sys.argv)):
    print(str(sys.argv[i]))




########## Quandl api_key
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




########## Quandl Code

code_COMP = "NASDAQOMX/COMP"
code_XCMP = "NASDAQOMX/XCMP"
code_NDX  = "NASDAQOMX/NDX"
code_XNDX = "NASDAQOMX/XNDX"




########## Get data from Nasdaq Data Link

df_COMP   = quandl.get(code_COMP)
df_XCMP   = quandl.get(code_XCMP)
df_NDX    = quandl.get(code_NDX)
df_XNDX   = quandl.get(code_XNDX)




########## View data and update data column ('Value') to an individual currency code


##### COMP
df_COMP = pd.DataFrame(df_COMP['Index Value'])
df_COMP = df_COMP.rename(columns={'Index Value': 'COMP'})
df_COMP.to_csv('df_COMP.csv', sep=',', header=True, index=True)


##### XCMP
df_XCMP = pd.DataFrame(df_XCMP['Index Value'])
df_XCMP = df_XCMP.rename(columns={'Index Value': 'XCMP'})
df_XCMP.to_csv('df_XCMP.csv', sep=',', header=True, index=True)


##### NDX
df_NDX = pd.DataFrame(df_NDX['Index Value'])
df_NDX = df_NDX.rename(columns={'Index Value': 'NDX'})
df_NDX.to_csv('df_NDX.csv', sep=',', header=True, index=True)


##### XNDX
df_XNDX = pd.DataFrame(df_XNDX['Index Value'])
df_XNDX = df_XNDX.rename(columns={'Index Value': 'XNDX'})
df_XNDX.to_csv('df_XNDX.csv', sep=',', header=True, index=True)




########## Combine raw data together

df_COMP_XCMP          = pd.merge(df_COMP, df_XCMP, on='Trade Date', how='outer')
df_COMP_XCMP_NDX      = pd.merge(df_COMP_XCMP, df_NDX, on='Trade Date', how='outer')
df_COMP_XCMP_NDX_XNDX = pd.merge(df_COMP_XCMP_NDX, df_XNDX, on='Trade Date', how='outer')


#### rename the pandas data frame to df_CCYs

df_EQ = df_COMP_XCMP_NDX_XNDX
#print(df_EQ)


df_EQ.sort_index(axis=0, ascending=True, inplace=True, na_position='last', ignore_index=False)


print(df_EQ.index)
'''
DatetimeIndex(['1999-03-04', '1999-03-05', '1999-03-08', '1999-03-09',
               '1999-03-10', '1999-03-11', '1999-03-12', '1999-03-15',
               '1999-03-16', '1999-03-17',
               ...
               '2021-07-15', '2021-07-16', '2021-07-19', '2021-07-20',
               '2021-07-21', '2021-07-22', '2021-07-23', '2021-07-26',
               '2021-07-27', '2021-07-28'],
              dtype='datetime64[ns]', name='Trade Date', length=5646, freq=None)
'''

print(df_EQ.columns)
'''
Index(['COMP', 'XCMP', 'NDX', 'XNDX'], dtype='object')
'''

#Drop rows when one or more columns have NaN.
df_EQ.dropna(inplace=True)


df_EQ.to_csv('df_EQ.csv', sep=',', header=True, index=True)




########## Calculate daily returns

#print(df_EUR_JPY_GBP_AUD_CAD_CHF.pct_change())

df_EQ_USD_Return = df_EQ.pct_change()
df_EQ_USD_Return.to_csv('df_EQ_USD_Return.csv', sep=',', header=True, index=True)




########## Calculate cumulative returns

df_EQ_USD_Cum_Return = (1 + df_EQ_USD_Return).cumprod()
#print(df_EQ_USD_Cum_Return)

df_EQ_USD_Cum_Return.to_csv('df_EQ_USD_Cum_Return.csv', sep=',', header=True, index=True)




########## Draw a graph of cumulative returns
df_EQ_USD_Cum_Return.plot(figsize=(12,9))
plt.ylabel("Cumulative Return (USD)")
plt.savefig("df_EQ_USD_Cum_Return.png")
plt.show()
plt.close("all")
