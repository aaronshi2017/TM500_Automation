import subprocess
from datetime import datetime
import time
import json
import os
import logging
from logging.handlers import TimedRotatingFileHandler

class class_moshellWSL:
    default_command = 'moshell 169.254.2.2 "uv com_usernames=rbs;uv com_passwords=rbs;lt all;st cell;deb cell;"'
    output = "No command output"

    def __init__(self):
        print("************** Moshell Command Execution *****************")
        self.command = self.default_command
    
    def setup_logging(self,output_folder):
        os.makedirs(output_folder, exist_ok=True)
        log_file = os.path.join(output_folder, 'moshell_commands.log')
        # Create a TimedRotatingFileHandler
        handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
        handler.setLevel(logging.INFO)
        
        # Create a formatter that includes the timestamp
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Get the root logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        # Remove any existing handlers
        if logger.hasHandlers():
            logger.handlers.clear()
        
        # Add the TimedRotatingFileHandler to the logger
        logger.addHandler(handler)

    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            logging.info(f"Command execution successfully!")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.info(f"Command execution got error: {e}")
            print(f"Error executing command: {e}")
            return None

    def command_execution(self, command):
        repo_path = "/home/rantechdev/TM500_Automation/TM500Automation"
        output_folder = os.path.join(repo_path, "output/moshell")
   
        # Configure logging
        self.setup_logging(output_folder)
        logging.info(f"original input command:{command}")
        # Input command should be a string
        self.command = f"{self.command[:-1]}{command}\""
        print(self.command)
        logging.info(f"final command:{self.command}")
        # Run the command
        time.sleep(5)
        self.output = self.execute_command(self.command)
        logging.info("=======================Command execution result======================")
        logging.info(f"{self.output}")
        
        # if self.output:
        #     # Generate json data to store the output
        #     data = {
        #         "command": command,
        #         "output": self.output
        #     }

            # # Get current timestamp
            # timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # # Specify the file paths with timestamp
            # output_dir = os.path.join("output", "json")
            # os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
            # file_path_json = os.path.join(output_dir, f"{timestamp}.json")

            # output_dir = os.path.join("output", "output_txt")
            # os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
            # file_path_txt = os.path.join(output_dir, f"{timestamp}.txt")

            # # Write data to JSON file
            # with open(file_path_json, "w") as json_file:
            #     json.dump(data, json_file, indent=4)  # indent parameter for pretty formatting

            # # Write output to text file
            # with open(file_path_txt, "w") as text_file:
            #     text_file.write(self.output)
        
        return self.output

if __name__ == "__main__":
    basictest = class_moshellWSL()
    basictest.command_execution("alt;")
