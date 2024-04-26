import requests
# Viavi test
# url = "http://127.0.0.1:5099/rtc/v2/tmas/0001/campaigns/actions/schedule"
# jsonData='{"TMA_TYPE": 1, "TMA_PATH": "C:/Program Files (x86)/VIAVI/TM500/5G NR - NLA 7.1.3/Test Mobile Application", "MCI_PORT":5003, "ACI_PORT": 5030, "TMA_PROFILE":"Profile1","ENABLE_RCE":1 ,"FILE_PATH": "C:/TMA_Sript/NSA - B7-N2.xml", "ITERATION_COUNT": 1,  "ACTION_ON_EVENT": 2,  "TESTS_SELECTION_BY_NAME": ["1UE-Attach"]}'
# # jsonData = '{"TMA_TYPE": 1, "TMA_PATH": "C:/Program Files (x86)/VIAVI/TM500/5G NR - NLA 7.1.3/Test Mobile Application", "MCI_PORT":5003, "ACI_PORT": 5030, "TMA_PROFILE":"Profile1","ENABLE_RCE":1}'
# Response = requests.post(url, data=jsonData,headers={"Content-Type":"application/json"})
# print(Response)

# API to open TMA
# Status: working but returning 404
url_openTMA = 'http://127.0.0.1:5099/rtc/v2/tmas' # working but returning 404
jsonData = '{"TMA_TYPE": 1}'
response = requests.post(url_openTMA,data=jsonData,headers={"Content-Type": "application/json"})
print(response)

# API: how to close TMA
#Test Result: working returning 200
# url_close='http://127.0.0.1:5099/rtc/v2/tmas'
# response = requests.delete (url_close,headers={"Content-Type":"application/json"}) 
# print(response)

# API to check campaign status
# Status: not working showing 404
url_status="http://127.0.0.1:5099/rtc/v2/tmas/0001/campaigns/LTE_Capacity_Simulation with XLE" # not working 404
jsonData = '{"TMA_TYPE": 1}'
response = requests.post(url_status,data=jsonData,headers={"Content-Type": "application/json"})
print(response)

# API to check TMA version
# Status: 
# url_instancecheck = 'http://localhost:5099/rtc/v2/version'
# response = requests.get(url_instancecheck, headers={"Content-Type":"application/json"})
# print(response)

# API to check TMA status when TMA is open
# Status: not working showing 404
url_instancecheck = 'http://localhost:5099/rtc/v2/tmas'
response = requests.get(url_instancecheck, headers={"Content-Type":"application/json"})
print(response)

# API to return TM500 location
# Status: 404 not working
url_location= 'http://localhost:5099/rtc/v2/tmas/0001'
response = requests.get(url_location, headers={"Content-Type":"application/json"})
print(response)

# API to schedule a campaign
# Status: 404 not working 
url_campaign_schedule ='http://127.0.0.1:5099/rtc/tmas/0001/campaigns/actions/schedule'
jsonData ='{"FILE_PATH":"C:\\TMA_Script\\NSA - B7-N2.xml","ITERATION_COUNT":1,"ACTION_ON_EVENT":2, "TESTS_SELECTION_BY_INDEX":[0]}'
Response = requests.post(url_campaign_schedule, data=jsonData,headers={"Content-Type":"application/json"})
print(Response)
