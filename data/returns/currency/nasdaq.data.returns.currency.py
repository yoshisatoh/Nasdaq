#################### Nasdaq Data Link : Get currency exchange rate data and calculate daily & cumulative USD returns ####################
#
#  (C) 2021, Yoshimasa (Yoshi) Satoh, CFA 
#
#  All rights reserved.
#
# Created:      2021/10/01
# Last Updated: 2021/10/01
#
# Github:
# https://github.com/yoshisatoh/Nasdaq/tree/main/data/returns/currency/nasdaq.data.returns.currency.py
#
#
########## Input Data Files
#
# You have to create a text file (api_key.txt) with only one line of Quandl' API key in it, and then save it on the same direcoty with this script (data.nasdaq.currency.returns.py)
#api_key.txt
#
# You do not need other input files as this program gets data from Nasdaq via the Internet by using the Quandl API key above.
#
#
########## Usage Instructions
#
#Run this py script on Windows Command Prompt as follows:
#python nasdaq.data.returns.currency.py
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
#SPOT EXCHANGE RATE - EURO AREA, Business day
#EUR/USD (USD per EUR)
#https://data.nasdaq.com/data/FED/RXI_US_N_B_EU-spot-exchange-rate-euro-area-business-day
#
#JAPAN -- SPOT EXCHANGE RATE, YEN/US$, Business day
#USD/JPY (JPY per USD)
#https://data.nasdaq.com/data/FED/RXI_N_B_JA-japan-spot-exchange-rate-yenus-business-day
#
#UNITED KINGDOM -- SPOT EXCHANGE RATE, US$/POUND (1/RXI_N.B.UK), Business day
#GBP/USD (USD per GBP)
#https://data.nasdaq.com/data/FED/RXI_US_N_B_UK-united-kingdom-spot-exchange-rate-uspound-1rxi_nbuk-business-day
#
#AUSTRALIA -- SPOT EXCHANGE RATE US$/AU$ (RECIPROCAL OF RXI_N.B.AL), Business day
#AUD/USD (USD per AUD)
#https://data.nasdaq.com/data/FED/RXI_US_N_B_AL-australia-spot-exchange-rate-usau-reciprocal-of-rxi_nbal-business-day
#
#CANADA -- SPOT EXCHANGE RATE, CANADIAN $/US$, Business day
#USD/CAD (CAD per USD)
#https://data.nasdaq.com/data/FED/RXI_N_B_CA-canada-spot-exchange-rate-canadian-us-business-day
#
#CHINA -- SPOT EXCHANGE RATE, YUAN/US$ P.R., Business day
#USD/CNY (CNY per USD)
#https://data.nasdaq.com/data/FED/RXI_N_B_CH-china-spot-exchange-rate-yuanus-pr-business-day
#
#SWITZERLAND -- SPOT EXCHANGE RATE, FRANCS/US$, Business day
#USD/CHF (CHF per USD)
#https://data.nasdaq.com/data/FED/RXI_N_B_SZ-switzerland-spot-exchange-rate-francsus-business-day
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
#
# If an exchange rate of a certain currency ('CCY') is denominated in USD, i.e., (USD per CCY), then a security code of the currency is experessed as
# code_CCY
#
# For instance, if you look at EUR, it is expressed as follows:
# EUR/USD (USD per EUR)
#
# Thus, a security code of EUR is
# code_EUR
#
#
# On the contrary, if an exchange rate of a certain currency ('CCY') is denominated in CCY, i.e., (CCY per USD), then a security code of the currency is experessed as
# code_USDCCY
#
# For instance, if you look at JPY, it is expressed as follows:
# USD/JPY (JPY per USD)
#
# Because of this, a security code of JPY is
# code_USDJPY
#
#
##### Set Nasdaq Data Link code
code_EUR    = "FED/RXI_US_N_B_EU"
code_USDJPY = "FED/RXI_N_B_JA"
code_GBP    = "FED/RXI_US_N_B_UK"
code_AUD    = "FED/RXI_US_N_B_AL"
code_USDCAD = "FED/RXI_N_B_CA"
code_USDCNY = "FED/RXI_N_B_CH"
code_USDCHF = "FED/RXI_N_B_SZ"




########## Get data from Nasdaq Data Link
df_EUR    = quandl.get(code_EUR)
df_USDJPY = quandl.get(code_USDJPY)
df_GBP    = quandl.get(code_GBP)
df_AUD    = quandl.get(code_AUD)
df_USDCAD = quandl.get(code_USDCAD)
df_USDCNY = quandl.get(code_USDCNY)
df_USDCHF = quandl.get(code_USDCHF)




########## View data and update data column ('Value') to an individual currency code


##### EUR
#
#print(type(df_EUR))
#<class 'pandas.core.frame.DataFrame'>
#
#print(df_EUR.index)
#print(df_EUR.columns)
'''
DatetimeIndex(['1999-01-04', '1999-01-05', '1999-01-06', '1999-01-07',
               '1999-01-08', '1999-01-11', '1999-01-12', '1999-01-13',
               '1999-01-14', '1999-01-15',
               ...
               '2021-09-03', '2021-09-07', '2021-09-08', '2021-09-09',
               '2021-09-10', '2021-09-13', '2021-09-14', '2021-09-15',
               '2021-09-16', '2021-09-17'],
              dtype='datetime64[ns]', name='Date', length=5700, freq=None)
Index(['Value'], dtype='object')
'''
#
df_EUR = df_EUR.rename(columns={'Value': 'EUR'})
df_EUR.to_csv('df_EUR.csv', sep=',', header=True, index=True)


##### JPY
#print(df_USDJPY.head())
#print(df_USDJPY['Value'].head())
#print(1/df_USDJPY['Value'].head())
#
df_JPY = df_USDJPY    # df_USDJPY['Value']: USD/JPY (JPY per USD)
df_JPY['Value'] = 1/df_USDJPY['Value']    # df_JPY['Value']: JPY/USD (USD per JPY)
#print(df_JPY['Value'].head())
#
df_JPY = df_JPY.rename(columns={'Value': 'JPY'})
df_JPY.to_csv('df_JPY.csv', sep=',', header=True, index=True)


##### GBP
df_GBP = df_GBP.rename(columns={'Value': 'GBP'})
df_GBP.to_csv('df_GBP.csv', sep=',', header=True, index=True)


##### AUD
df_AUD = df_AUD.rename(columns={'Value': 'AUD'})
df_AUD.to_csv('df_AUD.csv', sep=',', header=True, index=True)


##### CAD
df_CAD = df_USDCAD    # df_USDCAD['Value']: USD/CAD (CAD per USD)
df_CAD['Value'] = 1/df_USDCAD['Value']    # df_CAD['Value']: CAD/USD (USD per CAD)
#
df_CAD = df_CAD.rename(columns={'Value': 'CAD'})
df_CAD.to_csv('df_CAD.csv', sep=',', header=True, index=True)


##### CNY
df_CNY = df_USDCNY    # df_USDCNY['Value']: USD/CNY (CNY per USD)
df_CNY['Value'] = 1/df_USDCNY['Value']    # df_CNY['Value']: CNY/USD (USD per CNY)
#
df_CNY = df_CNY.rename(columns={'Value': 'CNY'})
df_CNY.to_csv('df_CNY.csv', sep=',', header=True, index=True)


##### CHF
df_CHF = df_USDCHF    # df_USDCHF['Value']: USD/CHF (CHF per USD)
df_CHF['Value'] = 1/df_USDCHF['Value']    # df_CHF['Value']: CHF/USD (USD per CHF)
#
df_CHF = df_CHF.rename(columns={'Value': 'CHF'})
df_CHF.to_csv('df_CHF.csv', sep=',', header=True, index=True)




########## Combine raw data together

df_EUR_JPY = pd.merge(df_EUR, df_JPY, on='Date', how='outer')
df_EUR_JPY_GBP = pd.merge(df_EUR_JPY, df_GBP, on='Date', how='outer')
df_EUR_JPY_GBP_AUD = pd.merge(df_EUR_JPY_GBP, df_AUD, on='Date', how='outer')
df_EUR_JPY_GBP_AUD_CAD = pd.merge(df_EUR_JPY_GBP_AUD, df_CAD, on='Date', how='outer')
df_EUR_JPY_GBP_AUD_CAD_CNY = pd.merge(df_EUR_JPY_GBP_AUD_CAD, df_CNY, on='Date', how='outer')
df_EUR_JPY_GBP_AUD_CAD_CNY_CHF = pd.merge(df_EUR_JPY_GBP_AUD_CAD_CNY, df_CHF, on='Date', how='outer')


#### rename the pandas data frame to df_CCYs
df_CCYs = df_EUR_JPY_GBP_AUD_CAD_CNY_CHF


#print(df_CCYs)


df_CCYs.sort_index(axis=0, ascending=True, inplace=True, na_position='last', ignore_index=False)


print(df_CCYs.index)
'''
DatetimeIndex(['1971-01-04', '1971-01-05', '1971-01-06', '1971-01-07',
               '1971-01-08', '1971-01-11', '1971-01-12', '1971-01-13',
               '1971-01-14', '1971-01-15',
               ...
               '2021-09-03', '2021-09-07', '2021-09-08', '2021-09-09',
               '2021-09-10', '2021-09-13', '2021-09-14', '2021-09-15',
               '2021-09-16', '2021-09-17'],
              dtype='datetime64[ns]', name='Date', length=12721, freq=None)
'''


print(df_CCYs.columns)
#Index(['EUR', 'JPY', 'GBP', 'AUD', 'CAD', 'CNY', 'CHF'], dtype='object')


#Drop rows when one or more columns have NaN.
df_CCYs.dropna(inplace=True)


df_CCYs.to_csv('df_CCYs.csv', sep=',', header=True, index=True)




########## Calculate daily returns

#print(df_EUR_JPY_GBP_AUD_CAD_CHF.pct_change())

df_CCYs__USD_Return = df_CCYs.pct_change()
df_CCYs__USD_Return.to_csv('df_CCYs__USD_Return.csv', sep=',', header=True, index=True)




########## Calculate cumulative returns

df_CCYs__USD_Cum_Return = (1 + df_CCYs__USD_Return).cumprod()
#print(df_CCYs__USD_Cum_Return)

df_CCYs__USD_Cum_Return.to_csv('df_CCYs__USD_Cum_Return.csv', sep=',', header=True, index=True)




########## Draw a graph of cumulative returns
df_CCYs__USD_Cum_Return.plot(figsize=(15,9))
plt.ylabel("Cumulative Return (USD)")
plt.savefig("df_CCYs__USD_Cum_Return.png")
plt.show()
plt.close("all")
