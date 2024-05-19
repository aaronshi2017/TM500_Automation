try:
    from robot.libraries.BuiltIn import BuiltIn
    from robot.libraries.BuiltIn import _Misc
    import robot.api.logger as logger
    from robot.api.deco import keyword
    import paramiko
    import time
    import json 
    from datetime import datetime
    ROBOT = False
except Exception:
    ROBOT = False

class class_moshellcommand:
    # define the class variants
    defaultcommand='/home/rantechdev/moshell/moshell 169.254.2.2 "uv com_usernames=rbs;uv com_passwords=rbs;lt all"'
    host="localhost"
    username="rantechdev"
    password='8200Dixie'
    output=""
    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    

    def __init__(self):
        # Automatically add the host key if not present
        paramiko.util.log_to_file('paramiko.log')
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
             # Connect to the SSH server
            self.ssh_client.connect(self.host, username=self.username, password=self.password)
            print("SSH connection is successful!")
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
        except paramiko.SSHException as e:
            print("Unable to establish SSH connection:", str(e))
        finally:
            pass
    
    def commandexecution(self,command):
        print(command)
        #Input command should be a list 
        self.defaultcommand=self.defaultcommand[:-1]+";"+command+ '"'
        print(self.defaultcommand)
        # Run the command
        stdin, stdout, stderr = self.ssh_client.exec_command(self.defaultcommand)
        time.sleep(5)
        # Read the output
        return_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        
        # Print the output
        print(f"Output of '{command}':")
        print(output)

        # Generate json data to store the output
        data={
            "command": command,
            "output":output
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
            text_file.write(output)

        return return_code
    
    @keyword
    def ssh_Close(self):
        try:
            print("SSH connection will be closed!")
            self.ssh_client.close()
            return 0
        except paramiko.SSHException as e:
            print("ssh close has error", str(e))
            return -1
        finally:
            pass

if __name__ == "__main__":
    basictest=class_moshellcommand()
    basictest.commandexecution("")