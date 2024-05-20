import xml.etree.ElementTree as ET
import os,re,glob

class SupportFunctions:
    def __init__(self):
        pass
    
    def rename_test_files_in_project_folders(self):
        # Recursively search for all subfolders named 'project'
        root_dir=".."
        for project_folder in glob.glob(os.path.join(root_dir, '**', 'Project'), recursive=True):
            # Find all files in the 'project' subfolder that start with 'test'
            for test_file in glob.glob(os.path.join(project_folder, 'test*')):
                # Get the directory and file name
                directory = os.path.dirname(test_file)
                filename = os.path.basename(test_file)
                # Construct the new file name
                new_filename = 'old_' + filename
                new_file_path = os.path.join(directory, new_filename)
                # Rename the file
                os.rename(test_file, new_file_path)
                print(f'Renamed: {test_file} to {new_file_path}')
    
    # Use following code to decide if this is a list of test names or test number 
    def check_list_type(self,lst):
        if isinstance(lst, list):
            if all(isinstance(item, (int)) for item in lst):
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
    
    def find_key_by_value(self,dictionary, target_value):
        for key, value in dictionary.items():
            if value == target_value:
                return key
        return None
    
    def find_message(self,log_message,pattern):
        match=re.search(pattern,log_message)
        if match:
            return log_message.rsplit(' ', 1)[-1]
        else:
            return False

    def extract_npi_strings_from_file(self,file_path):
        # Load and parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Regular expression pattern to match strings starting with "npi_"
        pattern = re.compile(r'npi_\S+')
        
        testcase_dict={}
        
        i=0
        # Find all <testName> elements and apply the regex
        for testName in root.findall('.//testName'):
            match = pattern.search(testName.text)
            if match:
                testcase_dict[match.group()]=i
                i+=1
                print(match)
        return testcase_dict

if __name__ == "__main__":
        # Example input values
    arg1 = "alt;st cell"
    arg2 = "C:\\Users\\rante\\Documents\\VIAVI\\TM500\\5G NR\\Test Mobile Application\\NLA7.4.3 Rev2\\MyCampaigns\\NPI_TC-01.xml"
    arg3 = ["1UE-Attach","1UE-UDP"]
    arg4 = 'TM500_Automaton_Auto_Generate1'
       
    support=SupportFunctions()
    result1,result2=support.is_valid_xml_file(support.windows_to_wsl_path(arg2))
    if result1:
        print(result2)
    else:
        print("Not valid XML path")
    wslpath=support.windows_to_wsl_path(arg2)
    my_dict=support.extract_npi_strings_from_file(wslpath)
    for key in my_dict.keys():
        print(f'Key: {key}, Value: {my_dict[key]}')


  