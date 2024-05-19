import subprocess
from datetime import datetime
import time
import json
import os

class class_moshellcommandWSL:
    default_command = 'moshell 169.254.2.2 "uv com_usernames=rbs;uv com_passwords=rbs;lt all;st cell;deb cell;"'
    output = "No command output"

    def __init__(self):
        print("************** Moshell Command Execution *****************")
        self.command = self.default_command

    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            return None

    def command_execution(self, command):
        print(command)
        # Input command should be a string
        self.command = f"{self.command[:-1]}{command}\""
        print(self.command)
        # Run the command
        time.sleep(5)
        self.output = self.execute_command(self.command)
        
        if self.output:
            # Generate json data to store the output
            data = {
                "command": command,
                "output": self.output
            }

            # Get current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Specify the file paths with timestamp
            output_dir = os.path.join("output", "json")
            os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
            file_path_json = os.path.join(output_dir, f"{command}_{timestamp}.json")

            output_dir = os.path.join("output", "output_txt")
            os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
            file_path_txt = os.path.join(output_dir, f"{command}_{timestamp}.txt")

            # Write data to JSON file
            with open(file_path_json, "w") as json_file:
                json.dump(data, json_file, indent=4)  # indent parameter for pretty formatting

            # Write output to text file
            with open(file_path_txt, "w") as text_file:
                text_file.write(self.output)
        
        return self.output

if __name__ == "__main__":
    basictest = class_moshellcommandWSL()
    basictest.command_execution("alt;")
