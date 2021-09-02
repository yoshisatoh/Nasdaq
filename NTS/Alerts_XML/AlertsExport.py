#  (C) 2021, Yoshimasa (Yoshi) Satoh, CFA 
#
#  All rights reserved.
#
# Created:      2021/08/26
# Last Updated: 2021/09/02
#
# Github:
# https://github.com/yoshisatoh/nasdaq/tree/main/NTS/Alerts_XML/AlertsExport.py
#
#
# Notes:
#
# First off, download an AlertsExport.zip file from a Nasdaq Trade Surveillance website for your company.
# For example, a zip file can be downloaded by using the following URL.
# https://<yourorganisation>.smartsbroker.com/cmss/citadel/exportAlerts?marketCode=asx&date=20210730&bundle=true&apiVersion=8&lookbackDays=6
#
# Second, unzip the AlertsExport.zip file on your computer. An AlertsExport directory will be created.
#
# Third, save this AlertsExport.py file to a directory where the AlertsExport directory is created.
# (This py file and the AlertsExport directory need to be saved on the same directory.
# 
# Finally, execute this script on your Command Prompt (Windows) or Terminal (MacOS) as follows.
# python AlertsExport.py
#
# If it is successful, the following files will be created:
# (market).(yyyymmdd).alerts.csv    -    Details of alerts for each day
# (market).all.alerts.csv    -    An aggregated file of all the (market).(yyyymmdd).alerts.csv files
# (market).all.alerts.counts.csv    -    Aggregated alert counts for each alert during a specified period of time
# (market).png    -    a bar chart (x: date, y: total alertCount per day)
# summary.markets.csv    -    (market), (yyyymmdd), (total alertCount per day)
# summary.markets.market.csv    -    (market)
# summary.total.csv    -    (total alertCount for a specific period of time - if you use an example URL above, that covers from 24th July 2021 to 30th July 2021, i.e., 7 = 6+1 calendar days)




#################### import library ####################
import xml.etree.ElementTree as ET
import csv
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
import sys
import glob
import os




#################### AlertsExport/summary.xml ####################


########## Loading summary.xml

# Load summary.xml file and treat as "tree"
tree = ET.parse('AlertsExport/summary.xml')

# Pull the root (topmost) element of the tree
root = tree.getroot()


########## Creating summary.total.csv (total alert count)
# Create summary.total.csv file for: alertCount (total alert count for a specified period)
with open('summary.total.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([root.find('total/alertCount').text])
    total_alertCount = root.find('total/alertCount').text
#
#print(f.closed)
#True
#
#print(total_alertCount)


########## Creating summary.markets.csv (market, yyyymmdd, daily alert count)
# Create summary.markets.csv file with three columns: marketCode, date, alertCount
with open('summary.markets.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    #
    for dir1 in root:
        for dir2 in dir1:
            for dir3 in dir2:
                #####
                # market:     dir2.attrib["marketCode"]
                # date:       dir3.attrib["date"]
                # alertCount: dir3.find("alertCount").text
                #
                writer.writerow([dir2.attrib["marketCode"], dir3.attrib["date"], dir3.find("alertCount").text])
                #####
#
#print(f.closed)
#True


# Check the generated summary.markets.csv file
with open('summary.markets.csv', 'r') as f:
    print(f.read())
'''
(market),(yyyymmdd),(alertCount)
...
'''
#print(f.closed)
#True


# Load summary.markets.csv
summarydt = pd.read_csv('summary.markets.csv', names=('market', 'date', 'alertCount'))
df1 = pd.DataFrame(summarydt)
#
#print(df1)
'''
  market      date  alertCount
0    (market)  (yyyymmdd)           (alertCount)
1    ...
...
'''



########## Creating summary.markets.market.csv (market)
# Extract all the markets
df2 = pd.DataFrame(df1.iloc[:, 0].unique())
#print(df2)
#print(type(df2))
#
df2.to_csv('summary.markets.market.csv', header=False, index=False)
ls2 = list(pd.read_csv('summary.markets.market.csv'))
#
#print(ls2)
#['(market)']
#
#print(len(ls2))
#
ln2 = len(ls2)
print(ln2)
#1
#
#print(ls2[0])
#'(market)'
#
#print(type(ls2[0]))
#<class 'str'>


########## Creating (market).png (x: day, y: daily alert count)
# Draw a bar chart
#
for n in range(ln2):
    #
    print(df1[df1['market'] == ls2[n]])
    #
    X = list(df1['date'])
    X = pd.to_datetime(X, format='%Y%m%d')
    #
    Y = list(df1['alertCount'])
    #
    # Plot the data using bar() method
    plt.figure(figsize=(10,5))
    plt.bar(X, Y, color='k')
    plt.title(ls2[n] + ': total alertCount = ' + total_alertCount)
    plt.xlabel("date")
    plt.ylabel("alertCount")
    #
    # Save the plot
    plt.savefig(ls2[n] + '.png')
    #
    # Show the plot
    plt.show()
#




#################### AlertsExport/(market)/(yyyymmdd)/alerts.xml ####################

#print(ls2[0])
#'(market)'

mkt = str(ls2[0])
#print(mkt)

#print(df1)
#print(type(df1))
#
#Delete dates with no alert
df1nz = df1[df1['alertCount'] != 0]
#
datelst = list(df1nz['date'])


########## Creating (market).(yyyymmdd).alerts.csv (alert id, market, date, alertTime, alert title)
for n in range(len(datelst)):
    #
    # Load alerts.xml file and treat as "tree"
    tree = ET.parse('AlertsExport/' + mkt + '/' + str(datelst[n]) + '/alerts.xml')
    #
    # Pull the root (topmost) element of the tree
    root = tree.getroot()
    #
    # Create (market).(yyyymmdd).alerts.csv files
    with open(mkt + '.' + str(datelst[n]) + '.alerts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        #
        #####
        # writer.writerow([dir1.attrib['id'], dir1.attrib['id'].split('-')[0], datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date(), dir1.attrib['id'].split('-')[2], dir1.find("alertTime").text.split('T')[1].split('+')[0], dir1.find("title").text, dir1.find("sources").find("source").find("target").find("primaryTarget").find("security").text])
        #
        # (column name):     (xml)
        # alert_id:          dir1.attrib['id']
        # market:            dir1.attrib['id'].split('-')[0]
        # date(yyyy-mm-dd):  datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date()
        # alertCount:        dir1.attrib['id'].split('-')[2]
        # time(HH:mm:ss.sss):dir1.find("alertTime").text.split('T')[1].split('+')[0]
        # title:             dir1.find("title").text
        # security:          dir1.find("sources").find("source").find("target").find("primaryTarget").find("security").text
        # partcipants>house: dir1.find("participants").find("house").text
        # partcipants>trader: dir1.find("participants").find("trader").text
        # partcipants>account>ref: dir1.find("participants").find("account").find("ref").text
        #
        ##### adding column names
        writer.writerow(["alert_id", "market", "date", "alertCount", "time", "title", "security", "house", "trader", "account_ref"])
        #####
        #
        numofalert = 0
        #
        for dir1 in root:
            #
            numofalert = numofalert + 1
            #
            #####
            # The following alerts are skipped as it does not have security code:
            #
            # NEW PRICE HIGH ON LAST TRADING DAY OF MONTH SUMMARY (HOUSE)
            # AFTER PROCESSING COMPLETE (HOUSE)
            #####
            if dir1.find("title").text == "NEW PRICE HIGH ON LAST TRADING DAY OF MONTH SUMMARY (HOUSE)":
                #break
                continue
            elif  dir1.find("title").text == "AFTER PROCESSING COMPLETE (HOUSE)":
                #break
                continue
            else:
                #
                #writer.writerow([dir1.attrib['id'], dir1.attrib['id'].split('-')[0], datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date(), dir1.attrib['id'].split('-')[2], dir1.find("alertTime").text.split('T')[1].split('+')[0], dir1.find("title").text, dir1.find("sources").find("source").find("target").find("primaryTarget").find("security").text, dir1.find("participants").find("house").text])
                #
                #print(dir1.find("participants").find("house") is None)
                #print(dir1.find("participants").find("trader") is None)
                #print(dir1.find("participants").find("account") is None)
                #
                if (not(dir1.find("participants").find("trader") is None) and not(dir1.find("participants").find("account") is None)):
                    #
                    writer.writerow([dir1.attrib['id'],
                                     dir1.attrib['id'].split('-')[0],
                                     datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date(),
                                     dir1.attrib['id'].split('-')[2], dir1.find("alertTime").text.split('T')[1].split('+')[0],
                                     dir1.find("title").text,
                                     dir1.find("sources").find("source").find("target").find("primaryTarget").find("security").text,
                                     dir1.find("participants").find("house").text,
                                     dir1.find("participants").find("trader").text,
                                     dir1.find("participants").find("account").find("ref").text])
                    #
                    #print(dir1.find("participants").find("trader").text)
                    #
                elif (not(dir1.find("participants").find("trader") is None) and (dir1.find("participants").find("account") is None)):
                    #
                    writer.writerow([dir1.attrib['id'],
                                     dir1.attrib['id'].split('-')[0],
                                     datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date(),
                                     dir1.attrib['id'].split('-')[2], dir1.find("alertTime").text.split('T')[1].split('+')[0],
                                     dir1.find("title").text,
                                     dir1.find("sources").find("source").find("target").find("primaryTarget").find("security").text,
                                     dir1.find("participants").find("house").text,
                                     dir1.find("participants").find("trader").text,
                                     'NA'])
                    #
                elif ((dir1.find("participants").find("trader") is None) and not(dir1.find("participants").find("account") is None)):
                    #
                    writer.writerow([dir1.attrib['id'],
                                     dir1.attrib['id'].split('-')[0],
                                     datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date(),
                                     dir1.attrib['id'].split('-')[2], dir1.find("alertTime").text.split('T')[1].split('+')[0],
                                     dir1.find("title").text,
                                     dir1.find("sources").find("source").find("target").find("primaryTarget").find("security").text,
                                     dir1.find("participants").find("house").text,
                                     'NA',
                                     dir1.find("participants").find("account").find("ref").text])
                    #
                else:
                    #
                    writer.writerow([dir1.attrib['id'],
                                     dir1.attrib['id'].split('-')[0],
                                     datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date(),
                                     dir1.attrib['id'].split('-')[2], dir1.find("alertTime").text.split('T')[1].split('+')[0],
                                     dir1.find("title").text,
                                     dir1.find("sources").find("source").find("target").find("primaryTarget").find("security").text,
                                     dir1.find("participants").find("house").text,
                                     'NA',
                                     'NA'])
                    #
                #
                #print(dir1.find("participants").find("house").text) if (dir1.find("participants").find("house").text) else print('NA')
                #print(dir1.find("participants").find("trader").text) if (dir1.find("participants").find("trader")) else print('NA')
                #print(dir1.find("participants").find("account").find("ref").text) if (dir1.find("participants").find("account")) else print('NA')
                #
                #if dir1.find("participants").find("house").text:
                #    print(dir1.find("participants").find("house").text)
                #else:
                #    print("NA")
                #####
            #
#
#print(f.closed)
#True
#




#################### Merging all the (market).(yyyymmdd).alerts.csv files into (market).all.alerts.csv, and then create (market).all.alerts.counts.csv ####################

#Deleting an old file: (market).all.alerts.csv
os.remove(mkt + '.' + 'all' + '.alerts.csv')

#Load all the files: (market).(yyyymmdd).alerts.csv
files = glob.glob(mkt + '.' + '*' + '.alerts.csv')

# Create (market).all.alerts.csv file
with open(mkt + '.' + 'all' + '.alerts.csv', 'w', newline='') as f_new:
    #
    ##### adding column names
    writer = csv.writer(f_new)
    writer.writerow(["alert_id", "market", "date", "alertCount", "time", "title", "security", "house", "trader", "account_ref"])
    #####
    #
    for f in files:
        with open(f, 'r', newline='') as f_org:
            #
            #Skipping header (first row)
            header = next(f_org)
            #
            f_new.write(f_org.read())
#
#print(f.closed)
#True
#


# Sorting (mkt).all.alerts.csv by using the keys "date" and "alertCount"
#
mkt_all_alerts = pd.read_csv(mkt + '.' + 'all' + '.alerts.csv')
#
#print(mkt_all_alerts)
#print(mkt_all_alerts.sort_values(by=["date", "alertCount"], ascending=[True, True]))
#
mkt_all_alerts = mkt_all_alerts.sort_values(by=["date", "alertCount"], ascending=[True, True])
mkt_all_alerts.to_csv(mkt + '.' + 'all' + '.alerts.csv', index=False)


# Creating (mkt).all.alerts.counts.csv - aggregated alert counts for each alert during a specified period of time
#
#print(mkt_all_alerts['title'].value_counts())
#print(type(mkt_all_alerts['title'].value_counts()))
#
mkt_all_alerts['title'].value_counts().to_csv(mkt + '.' + 'all' + '.alerts.counts.csv', header=True, index=True)
#
mkt_all_alerts_counts = pd.read_csv(mkt + '.' + 'all' + '.alerts.counts.csv')
#
#print(mkt_all_alerts_counts)
#print(pd.DataFrame(mkt_all_alerts_counts))
#print(pd.DataFrame(mkt_all_alerts_counts).iloc[:,0])
#print(pd.DataFrame(mkt_all_alerts_counts).iloc[:,1])

