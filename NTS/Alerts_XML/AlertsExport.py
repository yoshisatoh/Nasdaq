#  (C) 2021, Yoshimasa (Yoshi) Satoh, CFA 
#
#  All rights reserved.
#
# Created:      2021/08/26
# Last Updated: 2021/09/15
#
# Github:
# https://github.com/yoshisatoh/nasdaq/tree/main/NTS/Alerts_XML/AlertsExport.py
#
#
# Notes:
#
# First off, download an AlertsExport.zip file from a Nasdaq Trade Surveillance website for your company.
# For example, you can downloade a zip file if you replace <yourorganisation> with your company's specific ID.
# https://<yourorganisation>.smartsbroker.com/cmss/citadel/exportAlerts?marketCode=asx&date=20210730&bundle=true&apiVersion=8&lookbackDays=6
#
# Second, unzip the AlertsExport.zip file on your computer. An AlertsExport directory will be created.
#
# Third, save this AlertsExport.py file to a directory where the AlertsExport directory is created.
# (This py file and the AlertsExport directory need to be saved on the same directory.
# 
# Finally, execute this script on your Command Prompt (Windows) or Terminal (MacOS) as follows.
# python AlertsExport.py
# (Your environment might need python3 instead of python.)
#
# If it is successful, then following files will be created:
#
# (market).(yyyymmdd).alerts.csv    -    Details of alerts for each trading/business day
# (market).all.alerts.csv    -    An aggregated file of all the (market).(yyyymmdd).alerts.csv files
# (market).all.alerts.counts.csv    -    Aggregated alert counts for each alert during a specified time period
# (market).png    -    a bar chart (x: date, y: total alert counts per day)
# (market).all.alerts.counts.house.csv    -    Aggregated alert counts during a specified time period for certain columns: house
# (market).all.alerts.counts.house.account_ref.csv    -    Aggregated alert counts during a specified time period for certain columns: house, account_ref
# (market).all.alerts.counts.house.security.csv    -    Aggregated alert counts during a specified time period for certain columns: house, security
# (market).all.alerts.counts.house.trader.csv    -    Aggregated alert counts during a specified time period for certain columns: house, trader
# (market).all.alerts.counts.house.trader.account_ref.security.csv    -    Aggregated alert counts during a specified time period for certain columns: house, trader, account_ref, security
# summary.markets.csv    -    (market), (yyyymmdd), (total alert counts per calendar day)
# summary.markets.market.csv    -    (market)
# summary.total.csv    -    (total alert counts for a specific period of time - if you use an example URL above, that covers from 24th July 2021 to 30th July 2021, i.e., 7 = 6+1 calendar days)
#
# (market).all.alerts.marketCode.securityCode.type.oid.csv    -    An aggregated file for individual alerts with "alert_id", "marketCode", "securityCode", "type", and "oid". If there are multiple oid for a single alert_id, then there will be multiple rows with the same order_id.




#################### import libraries ####################
import xml.etree.ElementTree as ET
import csv
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
import sys
import glob
import os
import    pathlib




#################### AlertsExport/summary.xml ####################


########## Load summary.xml

# Load a summary.xml file for a specified time period, and treat as "tree"
tree = ET.parse('AlertsExport/summary.xml')

# Pull the root (topmost) element of the tree
root = tree.getroot()


########## Create summary.total.csv
with open('summary.total.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([root.find('total/alertCount').text])
    total_alertCount = root.find('total/alertCount').text
#
#print(f.closed)
#True


########## Create summary.markets.csv
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




########## Create summary.markets.market.csv
#
# Extract all the markets
df2 = pd.DataFrame(df1.iloc[:, 0].unique())
#
df2.to_csv('summary.markets.market.csv', header=False, index=False)
ls2 = list(pd.read_csv('summary.markets.market.csv'))
#
#
ln2 = len(ls2)




########## Create (market).png (x: day, y: daily alert count)
#
# Draw a bar chart
#
for n in range(ln2):
    #
    #print(df1[df1['market'] == ls2[n]])
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
    # Save the plot as a png file
    plt.savefig(ls2[n] + '.png')
    #
    # Show the plot
    plt.show()
#




#################### AlertsExport/(market)/(yyyymmdd)/alerts.xml ####################

mkt = str(ls2[0])

# Delete dates with no alert, which are usually non-trading/business days
df1nz = df1[df1['alertCount'] != 0]

datelst = list(df1nz['date'])


########## Creating (market).(yyyymmdd).alerts.csv (alert id, market, date, alertTime, alert title)
for n in range(len(datelst)):
    #
    # Load alerts.xml and treat as "tree"
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
        # add column names
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
            # The following alerts are skipped as it does NOT have security code:
            #
            # NEW PRICE HIGH ON LAST TRADING DAY OF MONTH SUMMARY (HOUSE)
            # AFTER PROCESSING COMPLETE (HOUSE)
            #
            #####
            if dir1.find("title").text == "NEW PRICE HIGH ON LAST TRADING DAY OF MONTH SUMMARY (HOUSE)":
                #break
                continue
                #
            elif  dir1.find("title").text == "AFTER PROCESSING COMPLETE (HOUSE)":
                #break
                continue
                #
            else:
                #
                # 1. both trader and account/ref are available
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
                #
                # 2. trader is available and account is NOT available
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
                #
                # 3. trader is NOT available and account is available
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
                #
                # 4. NEITHER trader nor account/ref is available
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
                #####
            #
#
#print(f.closed)
#True
#




#################### Merge all the (market).(yyyymmdd).alerts.csv files into (market).all.alerts.csv, and then create (market).all.alerts.counts.csv ####################

# Create an empty file, or overwrite if it already exists: (market).all.alerts.csv
empty_file = pathlib.Path(mkt + '.' + 'all' + '.alerts.csv')
empty_file.touch()
#
# Delete an old file if it exists: (market).all.alerts.csv
os.remove(mkt + '.' + 'all' + '.alerts.csv')

# Load all the files: (market).(yyyymmdd).alerts.csv
files = glob.glob(mkt + '.' + '*' + '.alerts.csv')

# Create (market).all.alerts.csv
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
            # Skip header (first row)
            header = next(f_org)
            #
            f_new.write(f_org.read())
#
#print(f.closed)
#True
#


# Sort (mkt).all.alerts.csv by the keys "date" and "alertCount" in ascending order
#
mkt_all_alerts = pd.read_csv(mkt + '.' + 'all' + '.alerts.csv')
#
mkt_all_alerts = mkt_all_alerts.sort_values(by=["date", "alertCount"], ascending=[True, True])
#
# Overwrite (mkt).all.alerts.csv
mkt_all_alerts.to_csv(mkt + '.' + 'all' + '.alerts.csv', index=False)


# Create (mkt).all.alerts.counts.csv
#
mkt_all_alerts_counts = pd.DataFrame(mkt_all_alerts['title'].value_counts()).rename(columns={'title': 'alerts'})
#
mkt_all_alerts_counts.to_csv(mkt + '.' + 'all' + '.alerts.counts.csv', header=True, index=True)
#
mkt_all_alerts_counts = pd.read_csv(mkt + '.' + 'all' + '.alerts.counts.csv')




#################### Refer to (market).all.alerts.csv, calculate aggregated alert counts for each set of columns, and then create csv files for each


##### (mkt).all.alerts.counts.house.csv
#
mkt_all_alerts_house = pd.DataFrame(mkt_all_alerts.groupby(['house']).size())
mkt_all_alerts_house.rename(columns={0: 'alerts'}, inplace=True)
mkt_all_alerts_house.to_csv(mkt + '.' + 'all' + '.alerts.counts.house.csv', header=True, index=True)


##### (mkt).all.alerts.counts.house.security.csv
#
mkt_all_alerts_house_security = pd.DataFrame(mkt_all_alerts.groupby(['house', 'security']).size())
mkt_all_alerts_house_security.rename(columns={0: 'alerts'}, inplace=True)
mkt_all_alerts_house_security.to_csv(mkt + '.' + 'all' + '.alerts.counts.house.security.csv', header=True, index=True)


##### (mkt).all.alerts.counts.house.trader.csv
#
mkt_all_alerts_house_trader = pd.DataFrame(mkt_all_alerts.groupby(['house', 'trader']).size())
mkt_all_alerts_house_trader.rename(columns={0: 'alerts'}, inplace=True)
mkt_all_alerts_house_trader.to_csv(mkt + '.' + 'all' + '.alerts.counts.house.trader.csv', header=True, index=True)


##### (mkt).all.alerts.counts.house.account_ref.csv
#
mkt_all_alerts_house_account_ref = pd.DataFrame(mkt_all_alerts.groupby(['house', 'account_ref']).size())
mkt_all_alerts_house_account_ref.rename(columns={0: 'alerts'}, inplace=True)
mkt_all_alerts_house_account_ref.to_csv(mkt + '.' + 'all' + '.alerts.counts.house.account_ref.csv', header=True, index=True)


##### (mkt).all.alerts.counts.house.trader.account_ref.security.csv
#
mkt_all_alerts_house_trader_account_ref_security = pd.DataFrame(mkt_all_alerts.groupby(['house', 'trader', 'account_ref','security']).size())
mkt_all_alerts_house_trader_account_ref_security.rename(columns={0: 'alerts'}, inplace=True)
mkt_all_alerts_house_trader_account_ref_security.to_csv(mkt + '.' + 'all' + '.alerts.counts.house.trader.account_ref.security.csv', header=True, index=True)




#################### AlertsExport/(market)/(yyyymmdd)/alerts.xml [reprise] ####################

########## Creating (market).all.alerts.oid.csv (alert id, message_type, message_oid)

path2 = './AlertsExport/'

files_dir2a = os.listdir(path2)
mkt2 = [f2a for f2a in files_dir2a if os.path.isdir(os.path.join(path2, f2a))][0]
print(mkt2)
#exit()


files_dir2b = os.listdir(path2 + mkt2 + '/')
datelst2 = [f2b for f2b in files_dir2b if os.path.isdir(os.path.join(path2 + mkt2 + '/', f2b))]
#print(datelst2)
#print(type(datelst2))
#print(sorted(datelst2))
datelst2 = sorted(datelst2)
#print(datelst2)
#exit()


# Create (market).all.alerts.marketCode.securityCode.type.oid.csv
with open(mkt2 + '.' + 'all' + '.alerts.marketCode.securityCode.type.oid.csv', 'w', newline='') as f_new2:
    #
    ##### adding column names
    writer2 = csv.writer(f_new2)
    writer2.writerow(["alert_id", "marketCode", "securityCode", "type", "oid"])
    #
    for n in range(len(datelst)):
        #
        print(str(datelst[n]))
        tree2 = ET.parse('AlertsExport/' + mkt2 + '/' + str(datelst[n]) + '/alerts.xml')
        #
        root2 = tree2.getroot()
        #
        for alert in root2.findall('alert'):
            #
            for message in alert.iter('message'):
                #
                #print(message.get('oid'))
                #print("alert: " + alert.get('id') + ", oid: " + message.get('oid'))
                writer2.writerow([alert.get('id'), message.get('marketCode'), message.get('securityCode'), message.get('type'), message.get('oid')])
                #
            #
        #
    #
#
#print(f_new2.closed)
#True


