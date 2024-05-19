import requests
import xml.etree.ElementTree as ET
import os, time, json, re
from datetime import datetime

class class_TMA_API:

################## Below are the constants for Testing ###################################
    baseURL = 'http://192.168.10.100:5099/rtc/v2/tmas'
    tmaType = 1
    relativeURIe500 = '/0001/campaigns/actions/'
    # tmaPath = "C:/Program Files (x86)/VIAVI/TM500/5G NR - NLA 6.23.0/Test Mobile Application"
    tmaPath="C:/Users/rante/Desktop/TM500_SW_TMA/NLA_7_4_3/Test Mobile Application"
    error_code=600
    scheduled=""
###########################################################################################
    def __init__(self) -> None:
        pass

    def check_TMA_Status(self):
    # API to check TMA status when TMA is open
        url_instancecheck = self.baseURL
        try:
            response = requests.get(url_instancecheck, headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("TMA either not open or API call failed!")
            else:
                print("TMA status check API call successful")
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response

    def open_TMA(self):
    # API to open TMA
        url_openTMA = self.baseURL
        jsonData = {"TMA_TYPE": self.tmaType,"TMA_PATH":self.tmaPath,"TMA_PROFILE": "Default User"}
        try:
            response = requests.post(url_openTMA,data=json.dumps(jsonData),headers={"Content-Type": "application/json"})
            time.sleep(15)
            if response.status_code!=201:
                print("TMA open API call failed!")
            else:
                print("TMA status open API call successful")
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response

    def check_TMA_location(self):
    #API to check TMA location
        url_location = self.baseURL + "/0001"
        try:
            response = requests.get(url_location, headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("TMA location query API failed!")
            else:
                print("TMA location query API call successful")
                print("TMA location is:")
                print('\t'+response.text)
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response
        
    def close_TMA(self):
    #API to close TMA
        url_location = self.baseURL
        try:
            response = requests.delete(url_location, headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("TMA close API failed!")
            else:
                print("TMA close API call is successful")
                print('\t'+response.text)
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response
        
    def schedule_campaign_new(self,campaignPath,testcaselist):
        # This is for test and troubleshooting purpose
        url_location = self.baseURL + "/0001/campaigns/actions/schedule"
        jsonData={
        "FILE_PATH": "C:\\Users\\rante\\Documents\\VIAVI\\TM500\\5G NR\\Test Mobile Application\\NLA6.23.0 Rev5\\MyCampaigns\\5G-TestCases.xml",
        "ITERATION_COUNT": 1,
        "ACTION_ON_EVENT": 2,
        "TESTS_SELECTION_BY_NAME": [
            "1UE-Attach",
            "1UE-UDP"
        ]}
        print(jsonData)
        try:
            response = requests.post(url_location,data=json.dumps(jsonData),headers={"Content-Type": "application/json"})
            print(response)
            jsonData = {"FILE_PATH": campaignPath,"ITERATION_COUNT": 1,"ACTION_ON_EVENT": 2, "TESTS_SELECTION_BY_NAME":testcaselist}
            jsonString=json.dumps(jsonData)
            print(jsonString)
            response = requests.post(url_location, data=jsonString, headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("TMA campaign scheduling is failed")
            else:
                print("TMA campaign scheduling is successful")
                print("TMA schedule ID is:")
                print('\t'+response.text)
                self.scheduled=response.text[1:]
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response
    

    def schedule_campaign(self,campaignPath,testcaselist=[]):
    # API to schedule by test case;testcaseList should be a list;or use default one so we schedule whole campaign

        url_location = self.baseURL + "/0001/campaigns/actions/schedule"

        wlsPath=self.windows_to_wsl_path(campaignPath)

        Is_valid_xml, checkResult=self.is_valid_xml_file(wlsPath)
        if Is_valid_xml:
            pass
        else:
            print(checkResult)
            return self.error_code,"Input Campaign path is invalid"

        listCheckResult=self.check_list_type(testcaselist)
        jsonData={}
        if listCheckResult=="List of strings": # Schedule per Name 
            print(testcaselist)
            jsonData = {"FILE_PATH": campaignPath,"ITERATION_COUNT": 1,"ACTION_ON_EVENT": 2, "TESTS_SELECTION_BY_NAME":testcaselist}
        elif listCheckResult=="List of numbers": # Schedule per index
            jsonData = {"FILE_PATH": campaignPath,"ITERATION_COUNT": 1,"ACTION_ON_EVENT": 2, "TESTS_SELECTION_BY_INDEX":testcaselist}
        elif listCheckResult=="Empty List": # Schedule whole campaign 
            jsonData = {"FILE_PATH": campaignPath,"ITERATION_COUNT": 1,"ACTION_ON_EVENT": 2}
        else:
            return self.error_code, "Input test case list is not valid!"
        
        print(jsonData)

        try:
            response = requests.post(url_location, data=json.dumps(jsonData), headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("TMA campaign scheduling is failed")
            else:
                print("TMA campaign scheduling is successful")
                print("TMA schedule ID is:")
                print('\t'+response.text)
                self.scheduled=response.text[1:]
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response
    
    def run_campaign(self):
    #API to run campaign 
        url_location = self.baseURL+"/0001/campaigns/actions/run"
        if self.scheduled=="":
            print("No campaign is scheduled!")
            return self.error_code,"No campaign is scheduled, can not execute RUN action!"
        
        jsonData = {"CAMPAIGN_NAME": self.scheduled,  "ADD_TO_ACTIVE_SCHEDULER": 1}
        
        try:
            response = requests.post(url_location, data=json.dumps(jsonData), headers={"Content-Type":"application/json"})
            if response.status_code!=202:
                print("TMA run campaign API failed!")
            else:
                print("TMA run campaign API call is successful")
                print('\t'+response.text)
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response
    
    def run_campaign_to_end(self):
    #API to run campaign and wait till the end 
        url_location = self.baseURL+"/0001/campaigns/actions/run"
        if self.scheduled=="":
            print("No campaign is scheduled!")
            return self.error_code,"No campaign is scheduled, can not execute RUN action!"
        
        jsonData = {"CAMPAIGN_NAME": self.scheduled,  "ADD_TO_ACTIVE_SCHEDULER": 1}
        
        try:
            response = requests.post(url_location, data=json.dumps(jsonData), headers={"Content-Type":"application/json"})
            if response.status_code!=202:
                print("TMA run campaign API failed!")
            else:
                print("TMA run campaign API call is successful")
                print('\t'+response.text)
                time.sleep(10)
                result_code,result_text=self.check_Running_Campaign()
                while result_text[-1]=="%":
                    # print(result_text)
                    result_code,result_text=self.check_Running_Campaign()
                print("Campaign is complete:"+self.scheduled)
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response
    
    def check_Running_Campaign(self):
        #API to check running campaign status 
        url_location = self.baseURL+"/0001/campaigns/actions/run"
        try:
            response = requests.get(url_location, headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("TMA check campaign running API failed!")
            else:
                print("TMA check campaign running API call is successful")
                print('\t'+response.text)
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response
        
    def stop_Running_Campaign(self):
        #API to stop running campaign status 
        url_location = self.baseURL+"/0001/campaigns/actions/stop"
        try:
            response = requests.post(url_location, headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("TMA stop campaign running API failed!")
            else:
                print("TMA stop campaign running API call is successful")
                print('\t'+response.text)
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response
    
    def generate_report(self):
    #API to generate report
        url_location = self.baseURL+"/0001/campaigns/actions/generatereport"
        if self.scheduled=="":
            print("No campaign is scheduled! No report will be generated!")
            return self.error_code,"Need to run campaign first!"
        
        jsonData = {"CAMPAIGN_NAME": self.scheduled}
        try:
            response = requests.post(url_location, data=json.dumps(jsonData), headers={"Content-Type":"application/json"})
            if response.status_code!=202:
                print("TMA report generation API failed!")
            else:
                print("TMA report generation API call is successful")
                print('\t'+response.text)
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response
        
    def get_status_report_generation(self):
    #API to generate report
        url_location = self.baseURL+"/0001/campaigns/actions/generatereport"      
        
        try:
            response = requests.get(url_location,headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("TMA report generation status check API failed!")
            else:
                print("TMA report generation status check API call is successful")
                print('\t'+response.text)
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response
        
    def generate_report_to_end(self):
    #API to generate report
        url_location = self.baseURL+"/0001/campaigns/actions/generatereport"
        if self.scheduled=="":
            print("No campaign is scheduled! No report will be generated!")
            return self.error_code,"Need to run campaign first!"
        
        jsonData = {"CAMPAIGN_NAME": self.scheduled}

        try:
            response = requests.post(url_location, data=json.dumps(jsonData), headers={"Content-Type":"application/json"})
            if response.status_code!=202:
                print("TMA report generation API failed!")
                return response.status_code,response.text
            else:
                print("TMA report generation API call is successful")
                print('\t'+response.text)
                time.sleep(10)
                result_code,result_text=self.get_status_report_generation()
                while result_text[-1]=="%":
                    # print(result_text)
                    result_code,result_text=self.get_status_report_generation()
                print("Report generation is complete:"+self.scheduled)
                return result_code,result_text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response
    
    def execute_MCI_command(self,command="#$$GET_SYSTEM_VERSION"):
    #API to execute MCI command
        url_location = self.baseURL+"/0001/campaigns/actions/executecommand"      
        jsonData = {"MCI_COMMAND":command,"CMD_TIMEOUT":10}
       
        try:
            response = requests.post(url_location,data=json.dumps(jsonData),headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("TMA MCI command execution API failed!")
            else:
                print("TMA MCI command execution API call is successful")
                print('\t'+response.text)
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response
        
    def send_to_Database(self,project,session,complete):
        url_location="http://192.168.10.100:3000/load_tm500_reports_test"
        jsonData={"projectname":project,"report_path":session,"completed":complete}
        
        try:
            response = requests.post(url_location,data=json.dumps(jsonData),headers={"Content-Type":"application/json"})
            if response.status_code!=200:
                print("Database API connection failed!")
            else:
                print("Database API call is successful")
                print('\t'+response.text)
            return response.status_code,response.text
        except requests.exceptions.RequestException as e:
            # Print the error if an exception occurred during the request
            print(f"Request Error: {e}")
            return self.error_code,e.response

    # Use following code to decide if this is a list of test names or test number 
    def check_list_type(self,lst):
        if isinstance(lst, list):
            if all(isinstance(item, (int, float)) for item in lst):
                return "List of numbers"
            elif all(isinstance(item, str) for item in lst):
                return "List of strings"
            elif len(lst)==0:
                return "Empty List"
            else:
                return "Mixed type list"
        else:
            return "Not a list"
    
    # Use following code to verify if it is a valid XML file with path

    def is_valid_xml_file(self,file_path):
    # Check if the file exists
        if not os.path.isfile(file_path):
            return False, "File does not exist"

        # Check if the file has .xml extension
        if not file_path.lower().endswith('.xml'):
            return False, "File is not an XML file"

        # Try to parse the XML file
        try:
            ET.parse(file_path)
        except ET.ParseError:
            return False, "Invalid XML content"
        
        return True, "Valid XML file"

    def windows_to_wsl_path(self,path):
        if path.startswith("\\") or (len(path) > 2 and path[1] == ":"):
            # Convert backslashes to forward slashes
            wsl_path = path.replace("\\", "/")
            
            # Convert drive letter to lowercase and prepend '/mnt/'
            wsl_path = "/mnt/" + wsl_path[0].lower() + wsl_path[2:]
            
            return wsl_path
        elif path.startswith("/mnt/"):
            return path
        else:
            return path

    
if __name__ == "__main__":
    basictest=class_TMA_API()
    # Test case1==================>
    # print(basictest.close_TMA())
    # print(basictest.open_TMA())
    # time.sleep(10)
    # print(basictest.check_TMA_Status())
    # print(basictest.check_TMA_location())
    # path2=r"C:\Users\rante\Documents\VIAVI\TM500\5G NR\Test Mobile Application\NLA6.23.0 Rev5\MyCampaigns\5G-TestCases.xml"
    # path1=r"C:\TMA_Script\aaron_NSA - B7-N2.xml"
    # testcase1=[1,2]
    # testcase2=["MultiSlice","1UE-UDP"]
    # testcase3=["1UE-UDP"]
    # print(basictest.is_valid_xml_file(basictest.windows_to_wsl_path(path2)))
    # print(basictest.schedule_campaign(path2,testcase1))
    # # print(basictest.run_campaign_to_end())
    # print(basictest.run_campaign())
    # time.sleep(60)
    # print(basictest.check_Running_Campaign())
    # print(basictest.stop_Running_Campaign())
    # print(basictest.schedule_campaign(path2,testcase2))
    # # print(basictest.run_campaign_to_end())
    # print(basictest.run_campaign())
    # time.sleep(60)
    # print(basictest.check_Running_Campaign())
    # print(basictest.stop_Running_Campaign())
    # print(basictest.schedule_campaign(path2,testcase3))
    # # print(basictest.run_campaign_to_end())
    # print(basictest.run_campaign())
    # time.sleep(60)
    # print(basictest.check_Running_Campaign())
    # print(basictest.stop_Running_Campaign())
    # print(basictest.generate_report_to_end())
    # print(basictest.schedule_campaign(path,testcase2))
    # print(basictest.schedule_campaign(path))
    # # print(basictest.is_valid_xml_file("/mnt/c/Users/rante/Documents/VIAVI/TM500/5G NR/Test Mobile Application/NLA7.4.3 Rev2/MyCampaigns/NPI_TC-06.xml"))
    # # print(basictest.schedule_campaign("/mnt/c/Users/rante/Documents/VIAVI/TM500/5G NR/Test Mobile Application/NLA7.4.3 Rev2/MyCampaigns/NPI_TC-06.xml",[0,1]))
    # # Test case2 ========================>
    # path2=r"C:\Users\rante\Documents\VIAVI\TM500\5G NR\Test Mobile Application\NLA6.23.0 Rev5\MyCampaigns\5G-TestCases.xml"
    # testcase2=["MultiSlice","1UE-UDP"]
    # print(basictest.schedule_campaign_new(path2,testcase2))

    # Test case 3=========================>
    print(basictest.send_to_Database("Aaron_Test4","240509_114618_session",False))