import subprocess
from datetime import datetime
import time
import json
class class_moshellcommandWSL:
    # define the class variants
    defaultcommand='moshell 169.254.2.2 "uv com_usernames=rbs;uv com_passwords=rbs;lt all;"'
    command=""
    output=""
    # Create an SSH client
  
    def __init__(self):
        print("************** Moshell Command Execution *****************")
        self.command=self.defaultcommand
        self.output="No command output"

    def execute_command(self,command):
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            return None
 
    def commandexecution(self,command):
        print(command)
        #Input command should be a string
        self.command=self.command[:-1]+command+'"'
        print(self.command)
        # Run the command
        time.sleep(5)
        self.output=self.execute_command(self.command)
        if self.output:
            # Generate json data to store the output
            data={
                "command": command,
                "output": self.output
            }
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Specify the file path with timestamp
        file_path1 = f".\output\json\{command}_{timestamp}.json"
        file_path2 = f".\output\output_txt\{command}_{timestamp}.txt"

        # Write data to JSON file
        with open(file_path1, "w") as json_file:
            json.dump(data, json_file, indent=4)  # indent parameter for pretty formatting

        with open(file_path2, "w") as text_file:
            text_file.write(self.output)  

if __name__ == "__main__":
    basictest=class_moshellcommandWSL()
    basictest.commandexecution("alt;")