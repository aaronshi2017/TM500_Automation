import requests
import json
import urllib3
import sys, os, time, json, re
from datetime import datetime, timedelta


####################################### Below are the constants for Testing #######################################
baseURI = '/rtc/v2/tmas'
server = '127.0.0.1:5099'
tmaType = '1'
transportType = 'http://'
relativeURIe500 = '/0001/campaigns/actions/'
relativeURIexMue = '/0001/tests/actions/'
tmaPath = "C:/Program Files (x86)/VIAVI/TM500/5G NR - NLA 7.1.3/Test Mobile Application"
campaignPath = "C:/Users/rante/Documents/VIAVI/TM500/5G NR/Test Mobile Application/NLA6.2.3 Rev1/MyCampaigns/5G-TestCases.xml"
grfPath = "C:/PyProjects/TMABins/TMA"
cName = "5G-TestCases.xml"
baseURL = transportType + server + baseURI
###########################################################################################

# API to check TMA status when TMA is open
# Status: not working showing 404
url_instancecheck = baseURL
response = requests.get(url_instancecheck, headers={"Content-Type":"application/json"})
print(response)
print(response.text)

####################### OPEN THE TMA ##############################################
#Status: working but returning 404

url_openTMA = baseURL # working but returning 404
jsonData = '{"TMA_TYPE": ' + tmaType + ', "TMA_PATH": "' + tmaPath + '", "MCI_PORT": 5003, "ACI_PORT": 5030, "TMA_PROFILE": "Default User"}'
response = requests.post(url_openTMA,data=jsonData,headers={"Content-Type": "application/json"})
print(response)
print(response.text)
time.sleep(10)

###################### SCHEDULE the CAMPAIGN ##########################################

# get date and time from system.  Note: timedelta adds seconds to the time to schedule the tests
# at a later time.  You can change this and put a static time in.  I am only using this for testing
# the code out so I do not have to statically type it in all the time.

date = datetime.now().date()
scheduleDate = str(date.month) + "/" + str(date.day) + "/" + str(date.year)
datetimeNow = datetime.now()
result = datetimeNow + timedelta(seconds=60)
print(result)  # 👉️ 2023-07-20 17:47:38.100856
print(result.time())  # 👉️ 17:47:38.100856
scheduleTime = f'{result:%H:%M:%S}'

# Viavi test # not working 404
url = baseURL + relativeURIe500 + "schedule"
jsonData = '{"FILE_PATH": "' + campaignPath + '", "DATE": "' + scheduleDate +'", "TIME": "' + scheduleTime +'", "ITERATION_COUNT": 1,"ACTION_ON_EVENT": 2}'
Response = requests.post(url, data=jsonData, headers={"Content-Type":"application/json"})
print(Response)
print(Response.text)

####################### CHECK CAMPAIGN STATUS ##################################
# Status: not working showing 404
url = baseURL + relativeURIe500 + 'run'
print(url)
# , "ADD_TO_ACTIVE_SCHEDULER":1
jsonData = '{"CAMPAIGN_NAME": "' + str(cName) + '"}'
response = requests.post(url, data=jsonData, headers={"Content-Type": "application/json"})
print(response)
print(response.text)
runCampaign = response.text

############################### CHECK RUNNING CAMPAIGN ##################################
# Note: This checks the running status of the campaign
count = 0

url = baseURL + relativeURIe500 + "run"
data = ''
if runCampaign != "No Campaign in progress":
    while (count < 10):
        getStatus = requests.get(url, data=data, headers={"Content-Type": "application/json"})
        print(getStatus.text)
        time.sleep(5)
        count += 1


######################### STOP the CAMPAIGN ###############################
url = baseURL + relativeURIe500 + 'stop'
data = ''
response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
print(response)
print(response.text)


######################### CLOSE THE TMA #############################
# API: how to close TMA
url_close= baseURL + "/0001"
response = requests.delete (url_close, headers={"Content-Type":"application/json"})
print(response)


########################## RETURN TMA LOCATION ############################
# API to return TM500 location
# Status: 404 not working
url_location = baseURL + "/0001"
response = requests.get(url_location, headers={"Content-Type":"application/json"})
print(response)


