import os,glob
from datetime import datetime
class PytestGeneration:

    project=""
    XMLpath=""
    testcases=None
    moshellcommand=""

    def __init__(self,project,XMLpath,testcases,moshellcommand):
        self.project=project
        self.XMLpath=XMLpath
        self.testcases=testcases
        self.moshellcommand=moshellcommand
    
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

    def generate_pytest_script(self):
        template="""
import pytest,time,re,os,sys

from ..modules.class_moshellWSL import class_moshellWSL
from ..modules.class_TMA_API import class_TMA_API


finalpath=""
finalverdict=""
sessionName=""

@pytest.fixture(scope="module")
def moshell_command():
    return class_moshellWSL()

@pytest.fixture(scope="module")
def TMA_API():
    return class_TMA_API()

def test_step1_command(moshell_command):
    result=moshell_command.command_execution("{arg1}")
    print(result)
    assert result is not None

def test_step2_close_TMA(TMA_API):
    result1,result2=TMA_API.close_TMA()
    print(result1,result2)
    assert result1==200

def test_step3_open_TMA(TMA_API):
    result1,result2=TMA_API.open_TMA()
    print(result1,result2)
    assert result1==201

def test_step4_check_TMA_status(TMA_API):
    time.sleep(5)
    result1,result2=TMA_API.check_TMA_Status()
    print(result1,result2)
    assert result1==200

def test_step5_check_TMA_location(TMA_API):
    result1,result2=TMA_API.check_TMA_location()
    print(result1,result2)
    assert result1==200

def test_step6_schedule_campaign(TMA_API):
    path=r"{arg2}"
    testcase={arg3}
    result1,result2=TMA_API.schedule_campaign(path,testcase)
    print(result1,result2)
    assert result1==200

def test_step7_run_campaign_to_end(TMA_API):
    result1,result2=TMA_API.run_campaign_to_end()
    print(result1,result2)
    assert result1==202

def test_step8_generate_report_to_end(TMA_API):
    result1, result2 = TMA_API.generate_report_to_end()
    print(result1, result2)
    assert result1 == 200
    
    finalpath_match = re.search(r'C:\\\.*_session', result2)
    finalpath = finalpath_match.group()
    sessionName=finalpath.split("\\\\")[-1]
    assert finalpath_match is not None, "Final path not found"
    if finalpath is not None:
        print("The report folder is:",sessionName)
        assert sessionName is not None
    else:
        print("No report path found")

    finalverdict = result2[-4:]
    print("The final verdict is", finalverdict)
    assert finalverdict=="PASS"

def test_step9_update_report_to_database(TMA_API):
    if finalverdict=="PASS":
        result1, result2 = TMA_API.send_to_Database("{arg4}",sessionName,False)
        print(result1,result2)
        assert result1 == 200
    else:
        print(finalverdict)
        assert finalverdict is not None

    """
        script_content = template.format(
            arg1=self.moshellcommand,
            arg2=self.XMLpath,
            arg3=self.testcases,
            arg4=self.project
        )
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        testname='test_'+self.project+'_'+timestamp+'.py'
        # Define the file path within the project folder
        base_dir = os.path.dirname(__file__)
        # Define the relative path to subfolder1 from the script's location
        relative_path_to_subfolder1 = os.path.join(base_dir, '../Project')
        file_path = os.path.join(relative_path_to_subfolder1, testname)
        self.rename_test_files_in_project_folders()
        try:
            with open(file_path, 'w') as f:
                f.write(script_content)        
            print("Pytest script is created successfully.")
            return testname
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    
if __name__ == "__main__":
    # Example input values
    arg1 = "alt;st cell"
    arg2 = "C:\\Users\\rante\\Documents\\VIAVI\\TM500\\5G NR\\Test Mobile Application\\NLA7.4.3 Rev2\\MyCampaigns\\NPI_TC-01.xml"
    arg3 = ["1UE-Attach","1UE-UDP"]
    arg4 = 'TM500_Automaton_Auto_Generate1'
    generate=PytestGeneration(arg4,arg2,arg3,arg1)
    generate.generate_pytest_script()


