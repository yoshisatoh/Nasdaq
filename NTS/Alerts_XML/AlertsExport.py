#  (C) 2021, Yoshimasa Satoh, CFA 
#
#  All rights reserved.
#
# Created:      2021/08/26
# Last Updated: 2021/08/30
#
# https://github.com/yoshisatoh/nasdaq/tree/main/NTS/Alerts_XML/AlertsExport.py
#
#
# Notes:
#
# First off, download AlertsExport.zip from your Nasdaq Trade Surveillance website. For example, the URL goes like this:
# https://<yourorganisation>.smartsbroker.com/cmss/citadel/exportAlerts?marketCode=asx&date=20210 730&bundle=true&apiVersion=8&lookbackDays=6
#
# This AlertsExport.py file has to be saved on the same directory as the AlertsExport directory is located.
# 
# Then execute this script on your Command Prompt (Windows) or Terminal (MacOS) as follows:
# python AlertsExport.py


# import library
import xml.etree.ElementTree as ET
import csv
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
import sys



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
    #writer.writerow([root.tag])
    #writer.writerow([root.attrib])
    #for dir1 in root:
        #writer.writerow([dir1.tag])
        #writer.writerow([dir1.attrib])
        #writer.writerow([dir1.find("alertCount")])
        #
        #for dir2 in dir1:
            #writer.writerow([dir2.tag])
            #print(root.find('total/alertCount').text)
            #writer.writerow([dir2.attrib])
            #
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
                #writer.writerow([dir3.attrib["date"], dir3.find("alertCount").text])
                writer.writerow([dir2.attrib["marketCode"], dir3.attrib["date"], dir3.find("alertCount").text])
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
#df1 = pd.DataFrame(summarydt)
df1 = pd.DataFrame(summarydt)
#print(df1)
'''
  market      date  alertCount
0    (market)  (yyyymmdd)           (alertCount)
1    ...
...
'''



########## Creating summary.markets.market.csv (market)
# Extract all the markets
#print(df1.iloc[:, 0].unique())
#print(type(df1.iloc[:, 0].unique()))
#<class 'numpy.ndarray'>
df2 = pd.DataFrame(df1.iloc[:, 0].unique())
#print(df2)
df2.to_csv('summary.markets.market.csv', header=False, index=False)
ls2 = list(pd.read_csv('summary.markets.market.csv'))
#
#print(ls2)
#['asx']
#
#print(len(ls2))
ln2 = len(ls2)
print(ln2)
#1
#
#print(ls2[0])
#asx
#
#print(type(ls2[0]))
#<class 'str'>



########## Creating (market).png (x: day, y: daily alert count)
# Draw a bar chart
#
for n in range(ln2):
    #
    #print(df1.query('market == "asx"'))
    #
    #print(df1[df1['market'] == 'asx'])
    print(df1[df1['market'] == ls2[n]])
    #
    #X = list(df1.iloc[:, 1])
    X = list(df1['date'])
    #print(type(df1['date']))
    #<class 'pandas.core.series.Series'>
    X = pd.to_datetime(X, format='%Y%m%d')
    #
    #Y = list(df1.iloc[:, 2])
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
#asx
mkt = str(ls2[0])
print(mkt)

print(df1)
print(type(df1))
#
#Delete dates with no alert
df1nz = df1[df1['alertCount'] != 0]
#
#print(df1['date'])
datelst = list(df1nz['date'])
#print(datelst)
#print(len(datelst))
#print(datelst[0])


########## Creating (market).(yyyymmdd).alerts.csv (alert id, market, date, alertTime, alert title)
for n in range(len(datelst)):
    #
    # Load alerts.xml file and treat as "tree"
    tree = ET.parse('AlertsExport/' + mkt + '/' + str(datelst[n]) + '/alerts.xml')
    #
    # Pull the root (topmost) element of the tree
    root = tree.getroot()
    #
    # Create summary.total.csv file for: alertCount (total alert count for a specified period)
    with open(mkt + '.' + str(datelst[n]) + '.alerts.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        #
        numofalert = 0
        #
        for dir1 in root:
            #
            #print(len(root))
            #number of the alerts
            #
            #print(dir1)
            #for dir2 in dir1:
                #
                #
            #writer.writerow([dir1.attrib['id'], dir1.find("title").text])
            #
            #print(type(dir1.attrib['id']))
            #<class 'str'>
            #
            #print(dir1.attrib['id'].split('-'))
            #['(market)', '(yyyymmdd)', '(id)']
            #
            #print(dir1.attrib['id'].split('-')[0])
            #'(market)'
            #
            #print(dir1.attrib['id'].split('-')[1])
            #'(yyyymmdd)'
            #print(type(dir1.attrib['id'].split('-')[1]))
            #<class 'str'>
            #
            #print(datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d'))
            #'(YYYY-mm-dd HH:mm:ss)'
            #
            #print(datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date())
            #'(YYYY-mm-dd)'
            #
            #print(dir1.attrib['id'].split('-')[2])
            #'(id)'
            #
            #writer.writerow([dir1.attrib['id'], dir1.attrib['id'].split('-')[0], dir1.attrib['id'].split('-')[1], dir1.attrib['id'].split('-')[2], dir1.find("title").text])
            #
            numofalert = numofalert + 1
            #print(numofalert)
            #
            #The last alert in a day, AFTER PROCESSING COMPLETE (HOUSE), will be ignored as it does not have security code.
            #if numofalert == len(root):
            #    break
            #
            ##########
            # The following alerts are skipped as it does not have security code:
            #
            # NEW PRICE HIGH ON LAST TRADING DAY OF MONTH SUMMARY (HOUSE)
            # AFTER PROCESSING COMPLETE (HOUSE)
            ##########
            if dir1.find("title").text == "NEW PRICE HIGH ON LAST TRADING DAY OF MONTH SUMMARY (HOUSE)":
                #break
                continue
            elif  dir1.find("title").text == "AFTER PROCESSING COMPLETE (HOUSE)":
                #break
                continue
            else:
                writer.writerow([dir1.attrib['id'], dir1.attrib['id'].split('-')[0], datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date(), dir1.attrib['id'].split('-')[2], dir1.find("alertTime").text.split('T')[1].split('+')[0], dir1.find("title").text, dir1.find("sources").find("source").find("target").find("primaryTarget").find("security").text])
            #
            #else:
                #
                #writer.writerow([dir1.attrib['id'], dir1.attrib['id'].split('-')[0], datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date(), dir1.attrib['id'].split('-')[2], dir1.find("alertTime").text.split('T')[1].split('+')[0], dir1.find("title").text])
                #
                #print([dir1.find("sources").text])
                #print([dir1.find("sources")])
                #print([dir1.find("sources").find("source").text])
                #print([dir1.find("sources").find("source").find("market").text])
                #print([dir1.find("sources").find("source").find("target").text])
                #print([dir1.find("sources").find("source").find("target").find("primaryTarget")])
                #print([dir1.find("sources").find("source").find("target").find("primaryTarget").find("security").text])
                #
                #writer.writerow([dir1.attrib['id'], dir1.attrib['id'].split('-')[0], datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date(), dir1.attrib['id'].split('-')[2], dir1.find("alertTime").text.split('T')[1].split('+')[0], dir1.find("title").text, dir1.find("sources").find("source").find("target").find("primaryTarget").find("security").text])
            #
            #writer.writerow([dir1.attrib['id'], dir1.attrib['id'].split('-')[0], datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date(), dir1.attrib['id'].split('-')[2], dir1.find("alertTime").text.split('T')[1].split('+')[0], dir1.find("title").text])
            ##writer.writerow([dir1.attrib['id'], dir1.attrib['id'].split('-')[0], datetime.datetime.strptime(dir1.attrib['id'].split('-')[1], '%Y%m%d').date(), dir1.attrib['id'].split('-')[2], dir1.find("alertTime").text.split('T')[1].split('+')[0], dir1.find("title").text, dir1.find("sources").find("source").find("target").find("primaryTarget").find("security").text])
            #print([dir1.find("sources").find("source").find("target").find("primaryTarget").find("security").text])
            #
            #
#
#print(f.closed)
#True
#
