import requests
import json
import urllib3
import sys, os, time, json, re
from datetime import datetime, timedelta

class class_TMA_API:

################## Below are the constants for Testing ###################################
    baseURL = 'http://127.0.0.1:5099/rtc/v2/tmas'
    tmaType = '1'
    relativeURIe500 = '/0001/campaigns/actions/'
    tmaPath = "C:/Program Files (x86)/VIAVI/TM500/5G NR - NLA 6.23.0/Test Mobile Application"
    grfPath = "C:/PyProjects/TMABins/TMA"
    cName = "5G-TestCases.xml"
###########################################################################################

    def __init__(self) -> None:
        pass

    def check_TMA_Status(self):
    # API to check TMA status when TMA is open
        url_instancecheck = self.baseURL
        try:
            response = requests.get(url_instancecheck, headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("TMA status check API call failed!")
                return response.status_code
            elif response.text!="0001":
                # if TMA status shows not open, try open it 
                # For now, we are trying API call to TMA v6.23
                openstatus=self.open_TMA()
                if openstatus==200:
                    self.check_TMA_Status()
                else:
                    return openstatus
            else:
                print("TMA status check API call successful")
                return response.text
        except:
            print("Something wrong")
            return None

    def open_TMA(self):
    # API to open TMA
        url_openTMA = self.baseURL
        jsonData = '{"TMA_TYPE": ' + self.tmaType + ', "TMA_PATH": "' + self.tmaPath + '", "TMA_PROFILE": "Default User"}'
        try:
            response = requests.post(url_openTMA,data=jsonData,headers={"Content-Type": "application/json"})
            time.sleep(10)
            if response.status_code!=200:
                print("TMA open API call failed!")
                return response.status_code
            else:
                print("TMA status check API call successful")
                return response.status_code
        except:
            print("Something wrong")
            return -1

    def check_TMA_location(self):
    #API to check TMA location
        url_location = self.baseURL + "/0001"
        try:
            response = requests.get(url_location, headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("TMA location query API failed!")
                return response.status_code
            else:
                print("TMA location query API call successful")
                print("TMA location is:")
                print('\t'+response.text)
                return response.status_code
        except:
            print("Something wrong")
            return -1

    def schedule_campaign(self,campaignPath,testcaseName):
    # API to schedule by test case
    # testcaseName should be a list
        url_location = self.baseURL + "/0001/campaigns/actions/schedule"
        jsonData = '{"FILE_PATH": "' + campaignPath + '", "ITERATION_COUNT": 1,"ACTION_ON_EVENT": 2}'

        try:
            response = requests.get(url_location, data=jsonData, headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("TMA location query API failed!")
                return response.status_code
            else:
                print("TMA location query API call successful")
                print("TMA location is:")
                print('\t'+response.text)
                return response.status_code
        except:
            print("Something wrong")
            return -1

    {
  "FILE_PATH": "C:\\TMA_Script\\aaron_NSA - B7-N2.xml",
  "ITERATION_COUNT": 1,
  "ACTION_ON_EVENT": 2,
  "TESTS_SELECTION_BY_INDEX": [ 0, 1  ]
}


# Viavi test # not working 404
url = baseURL + relativeURIe500 + "schedule"
jsonData = '{"FILE_PATH": "' + campaignPath + '", "DATE": "' + scheduleDate +'", "TIME": "' + scheduleTime +'", "ITERATION_COUNT": 1,"ACTION_ON_EVENT": 2}'
Response = requests.post(url, data=jsonData, headers={"Content-Type":"application/json"})
print(Response)
print(Response.text)

if __name__ == "__main__":
    basictest=class_TMA_API()
    basictest.check_TMA_location()