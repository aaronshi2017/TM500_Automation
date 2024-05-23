from flask import Flask, jsonify, request
import logging,time,os,yaml
from logging.handlers import TimedRotatingFileHandler
from modules.class_supportFunctions import SupportFunctions
from modules.class_pytestGenerate import PytestGeneration
import func_gitUpload
from modules.class_moshellWSL import class_moshellWSL

app = Flask(__name__)

# # Configure logging
log_directory = './applogs/'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_message = super().format(record)
        return log_message.replace('\\n', '\n')  # Ensure new lines are correctly formatted

# Configure logging
log_handler = TimedRotatingFileHandler(os.path.join(log_directory, 'app_API.log'), when='midnight', interval=1, backupCount=7)
log_handler.setLevel(logging.INFO)

# Define the log message format
formatter = CustomFormatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
log_handler.setFormatter(formatter)
# Ensure the root logger is configured to capture logs
logging.basicConfig(level=logging.INFO, handlers=[log_handler])
# if not any(isinstance(handler, TimedRotatingFileHandler) for handler in app.logger.handlers):
#     app.logger.addHandler(log_handler)
# Ensure the handler is only added once and prevent propagation
if not app.logger.handlers:
    app.logger.addHandler(log_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.propagate = False
support_function=SupportFunctions()

@app.before_request
def log_request_info():
    app.logger.info(f'{request.remote_addr} - - [{time.strftime("%d/%b/%Y %H:%M:%S")}] "{request.method} {request.path} {request.scheme.upper()}/{request.environ.get("SERVER_PROTOCOL")}"')

@app.after_request
def log_response_info(response):
    app.logger.info(f'{request.remote_addr} - - [{time.strftime("%d/%b/%Y %H:%M:%S")}] "{request.method} {request.path} {request.scheme.upper()}/{request.environ.get("SERVER_PROTOCOL")}" {response.status_code} -')
    return response

def process_arguments(project,xmlPath,testcases,moshellcommand):
    pytestScript=PytestGeneration(project,xmlPath,testcases,moshellcommand)
    support_function.rename_test_files_in_project_folders() #mark previous test files as old_
    result=pytestScript.generate_pytest_script()

    if result:
        # github=class_gitHubUpload(project)
        # github.github_upload()
        # Upload the new files to Github 
        if func_gitUpload.sync_remote_with_local(project, remote_name='origin', branch_name='featurebranch'):
            app.logger.info(f'Sync to Github successfully!')
            print("Sync completed successfully.")
        else:
            print("An error occurred during sync.")
            app.logger.info(f'An error occurred during Github sync!')
        return result
    else:
        return False

def read_yaml(file_path):
    with open(file_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
            app.logger.info("Read YAML file successfully!")
            return config
        except yaml.YAMLError as exc:
            print(f"Error reading YAML file: {exc}")
            app.logger.info("Read YAML file error!")
            return None
    
@app.route('/yaml',methods=['POST'])
def yaml_handle():
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    data = request.get_json()
    app.logger.info(f'Yaml test case files: {data}')
    yamlfile = data.get('Yaml')
    wslYamlfile=support_function.windows_to_wsl_path(yamlfile)
    config=read_yaml(wslYamlfile)
    if config:
        support_function.rename_test_files_in_project_folders() #mark previous test files as archived_
        support_function.savefile_YAML(wslYamlfile)
        for test_case in config['test_cases']:
            ID=test_case['id']
            Project=test_case['Project']
            XMLpath=test_case['XMLpath']
            Testcase=test_case['Test_cases']
            Moshell=test_case['Moshell']
            pytestScript=PytestGeneration(ID,Project,XMLpath,Testcase,Moshell)
            time.sleep(1)
            result=pytestScript.generate_pytest_script()
        if func_gitUpload.sync_remote_with_local("Yaml", remote_name='origin', branch_name='featurebranch'):
            app.logger.info(f'Sync to Github successfully!')
            print("Sync completed successfully.")
        else:
            print("An error occurred during sync.")
            app.logger.info(f'An error occurred during Github sync!')
            return jsonify({'error': 'Yaml file sync to Github failed!'}),400
        return jsonify({'result': 'Yaml file processed!'})
    else:
        app.logger.info(f'Yaml file validation has error: {data}')
        return jsonify({"error": "Yaml file validation error!"}), 400 


@app.route('/moshell',methods=['POST'])
def moshell():
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Get JSON data from the request
    data = request.get_json()
    app.logger.info(f'moshell {data["Moshell commands"]}')
    app.logger.info('************** Moshell Command Execution *****************')
    inputCommands = data.get('Moshell commands')
    default_command = 'moshell 169.254.2.2 "uv com_usernames=rbs;uv com_passwords=rbs;lt all;"'
    finalcommand = f"{default_command[:-1]}{inputCommands}\""
    print(finalcommand)
    moshell_obj=class_moshellWSL()
    moshell_result=moshell_obj.execute_command(finalcommand)
    if moshell_result:
        app.logger.info(f'{moshell_result}')
        return jsonify({'result': 'Moshell command execution\n:'+moshell_result})
    else:
        return jsonify({"error": "Something wrong"}), 400 
    

@app.route('/testbuild', methods=['POST'])
def api():

    # supportFunction=SupportFunctions()

    # Check if the request contains JSON data
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    # Get JSON data from the request
    data = request.get_json()
    project = data.get('Project')
    XMLpath = data.get('XMLPath')
    testcases = data.get('TestCases')
    moshellcommand=data.get('Moshellcommand')
    
    app.logger.info('************** Input Info*****************')
    app.logger.info(f'Project: {data["Project"]}')
    app.logger.info(f'XMLPath: {data["XMLPath"]}')
    app.logger.info(f'TestCases: {data["TestCases"]}')
    app.logger.info(f'Moshellcommand: {data["Moshellcommand"]}')

    if type(project) != str:
        return jsonify({"error": "Invalid Project Name!"}), 400
    
    WSLpath=support_function.windows_to_wsl_path(XMLpath)
    
    XMLpath_validation, XMLpath_result=support_function.is_valid_xml_file(WSLpath)
    if not XMLpath_validation:
        app.logger.info(f'XML path validation failed: {XMLpath_result}')
        return jsonify({"error": XMLpath_result}), 400 

    listtype=support_function.check_list_type(testcases)
    if not (listtype=="List of numbers" or listtype=="List of strings" or listtype=="Empty List"):
        app.logger.info(f'Test cases are not a list of valid test case string: {listtype}')
        return jsonify({"error": listtype}), 400 
    
    if type(moshellcommand) != str:
        app.logger.info(f'Moshell command is not a string of commands: {moshellcommand}')
        return jsonify({"error": "Invalid Project Name!"}), 400

    # Call the Python function with the arguments
    result=process_arguments(project,XMLpath,testcases,moshellcommand)
    if result:
        app.logger.info(f'Pytest script generated successfully: {result}')
        return jsonify({'result': 'Pytest script generated successfully:'+result})
    else:
        app.logger.info(f'Pytest script generated failed: {result}')
        return jsonify({"error": "No pytest script is generated"}), 400 
  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000,debug=True)

