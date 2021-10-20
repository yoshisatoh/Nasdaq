#################### Nasdaq Data Link : Get currency exchange rate data and calculate daily & cumulative USD returns ####################
#
#  (C) 2021, Yoshimasa (Yoshi) Satoh, CFA 
#
#  All rights reserved.
#
# Created:      2021/10/20
# Last Updated: 2021/10/20
#
# Github:
# https://github.com/yoshisatoh/Nasdaq/tree/main/data/returns/Bitcoin/nasdaq.data.returns.Bitcoin.py
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
#python nasdaq.data.returns.Bitcoin.py
#
#
########## Output Data Files
#
#df_BTC_price.csv
#df_BTC_volume.csv
#df_BTC_price_volume.csv
#df_BTC_price_USD_Return.csv
#df_BTC_price_USD_Cum_Return.csv
#df_BTC_price_volume_daily_cum_USD_ret.csv
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
#Bitcoin Market Price USD
#https://data.nasdaq.com/data/BCHAIN/MKPRU-bitcoin-market-price-usd
#
#Bitcoin USD Exchange Trade Volume
#https://data.nasdaq.com/data/BCHAIN/TRVOU-bitcoin-usd-exchange-trade-volume
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
import matplotlib.cm as cm
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




########## Nasdaq Data Link (formerly known as Quandl) Code
#
##### Set Nasdaq Data Link code
code_BTC_price    = "BCHAIN/MKPRU"
code_BTC_volume   = "BCHAIN/TRVOU"




########## Get data from Nasdaq Data Link
df_BTC_price     = quandl.get(code_BTC_price)
df_BTC_volume    = quandl.get(code_BTC_volume)




########## View data and update data column ('Value') to an individual currency code


##### BTC_price
#
#print(type(df_BTC_price))
#<class 'pandas.core.frame.DataFrame'>
#
#print(df_BTC_price.index)
#print(df_BTC_price.columns)
'''
DatetimeIndex(['2009-01-02', '2009-01-03', '2009-01-04', '2009-01-05',
               '2009-01-06', '2009-01-07', '2009-01-08', '2009-01-09',
               '2009-01-10', '2009-01-11',
               ...
               '2021-10-10', '2021-10-11', '2021-10-12', '2021-10-13',
               '2021-10-14', '2021-10-15', '2021-10-16', '2021-10-17',
               '2021-10-18', '2021-10-19'],
              dtype='datetime64[ns]', name='Date', length=4674, freq=None)
Index(['Value'], dtype='object')
'''
#
df_BTC_price  = df_BTC_price.rename(columns={'Value': 'Price'})
#
#Drop rows when price is zero.
df_BTC_price = df_BTC_price[df_BTC_price['Price'] != 0]

df_BTC_price.to_csv('df_BTC_price.csv', sep=',', header=True, index=True)

df_BTC_volume = df_BTC_volume.rename(columns={'Value': 'Volume'})
df_BTC_volume.to_csv('df_BTC_volume.csv', sep=',', header=True, index=True)




########## Combine raw data together

df_BTC_price_volume = pd.merge(df_BTC_price, df_BTC_volume, on='Date', how='outer')

df_BTC_price_volume.sort_index(axis=0, ascending=True, inplace=True, na_position='last', ignore_index=False)


print(df_BTC_price_volume.index)
'''
DatetimeIndex(['2009-01-02', '2009-01-03', '2009-01-04', '2009-01-05',
               '2009-01-06', '2009-01-07', '2009-01-08', '2009-01-09',
               '2009-01-10', '2009-01-11',
               ...
               '2021-10-10', '2021-10-11', '2021-10-12', '2021-10-13',
               '2021-10-14', '2021-10-15', '2021-10-16', '2021-10-17',
               '2021-10-18', '2021-10-19'],
              dtype='datetime64[ns]', name='Date', length=4674, freq=None)
'''


print(df_BTC_price_volume.columns)
#Index(['Price', 'Volume'], dtype='object')

#Drop rows when one or more columns have NaN.
df_BTC_price_volume.dropna(inplace=True)

df_BTC_price_volume.to_csv('df_BTC_price_volume.csv', sep=',', header=True, index=True)




########## Calculate daily returns

df_BTC_price_USD_return = df_BTC_price.pct_change()
df_BTC_price_USD_return.to_csv('df_BTC_price_USD_return.csv', sep=',', header=True, index=True)
df_BTC_price_USD_return  = df_BTC_price_USD_return.rename(columns={'Price': 'Daily_Return'})



########## Calculate cumulative returns

df_BTC_price_USD_cum_return = (1 + df_BTC_price_USD_return).cumprod()

df_BTC_price_USD_cum_return  = df_BTC_price_USD_cum_return.rename(columns={'Daily_Return': 'Cum_Return'})

df_BTC_price_USD_cum_return.to_csv('df_BTC_price_USD_cum_return.csv', sep=',', header=True, index=True)




########## Combine raw data and daily & cumulative returns together

df_BTC_price_volume_daily_USD_ret     = pd.merge(df_BTC_price_volume, df_BTC_price_USD_return, on='Date', how='outer')
df_BTC_price_volume_daily_cum_USD_ret = pd.merge(df_BTC_price_volume_daily_USD_ret, df_BTC_price_USD_cum_return, on='Date', how='outer')

df_BTC_price_volume_daily_cum_USD_ret.sort_index(axis=0, ascending=True, inplace=True, na_position='last', ignore_index=False)

df_BTC_price_volume_daily_cum_USD_ret.to_csv('df_BTC_price_volume_daily_cum_USD_ret.csv', sep=',', header=True, index=True)




########## Draw a graph of cumulative returns

#print(df_BTC_price_volume_daily_cum_USD_ret.index)
'''
DatetimeIndex(['2009-01-02', '2009-01-03', '2009-01-04', '2009-01-05',
               '2009-01-06', '2009-01-07', '2009-01-08', '2009-01-09',
               '2009-01-10', '2009-01-11',
               ...
               '2021-10-10', '2021-10-11', '2021-10-12', '2021-10-13',
               '2021-10-14', '2021-10-15', '2021-10-16', '2021-10-17',
               '2021-10-18', '2021-10-19'],
              dtype='datetime64[ns]', name='Date', length=4674, freq=None)
'''
#
#print(df_BTC_price_volume_daily_cum_USD_ret.columns)
'''
Index(['Price', 'Volume', 'Daily_Return', 'Cum_Return'], dtype='object')
'''
#print(df_BTC_price_volume_daily_cum_USD_ret['Cum_Return'].tail())

'''
#df_BTC_price_volume_daily_cum_USD_ret.plot(figsize=(15,9))

plt.figure(num=1, figsize=(15,9))


plt.plot(df_BTC_price_volume_daily_cum_USD_ret.index, df_BTC_price_volume_daily_cum_USD_ret['Cum_Return'], label='Cum_Return')
plt.plot(df_BTC_price_volume_daily_cum_USD_ret.index, df_BTC_price_volume_daily_cum_USD_ret['Volume'], label='Volume')

plt.legend()
plt.ylabel("Cumulative Return (USD)")
plt.savefig("df_BTC_price_volume_daily_cum_USD_ret.png")
plt.show()
plt.close("all")
'''




fig = plt.figure(num=1, figsize=(15,9))
ax1 = fig.add_subplot(111)

#t = np.linspace(0.0,10.0,1000)
t = df_BTC_price_volume_daily_cum_USD_ret.index

fs = 1.0


##### Line 1: Cumulative Returns
y1 = df_BTC_price_volume_daily_cum_USD_ret['Cum_Return']
ln1=ax1.plot(t, y1,'C0',label='Cum_Return')


##### Line 2: Volume
ax2 = ax1.twinx()
y2 = df_BTC_price_volume_daily_cum_USD_ret['Volume']
ln2=ax2.plot(t,y2,'C1',label='Volume')

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='upper left')

ax1.set_xlabel('Date')
ax1.set_ylabel('Cum_Return')
ax1.grid(True)
ax2.set_ylabel('Volume')

plt.savefig('Fig_1.png')
plt.show()
