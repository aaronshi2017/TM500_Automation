import os
import subprocess
import logging
from logging.handlers import TimedRotatingFileHandler

def run_git_command(command, repo_path):
    try:
        os.chdir(repo_path)
        # Execute the command and capture the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout.strip()

        # Log the output
        logging.info(f"Command: {command}")
        logging.info(f"Output: {output}")

        return (True, output)
    except Exception as e:
        logging.error(f"Error executing command: {e}")
        return (False, str(e))

def setup_logging(output_folder):
    os.makedirs(output_folder, exist_ok=True)
    log_file = os.path.join(output_folder, 'github_commands.log')
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

def sync_remote_with_local(project='test', remote_name='origin', branch_name='featurebranch'):
    # Specify the output folder for logs
    repo_path = "/home/rantechdev/TM500_Automation/TM500Automation"
    output_folder = os.path.join(repo_path, "output/github")
   
    # Configure logging
    setup_logging(output_folder)
    
    logging.info("Starting sync process")
    
    success, _ = run_git_command('git status', repo_path)
    if success:
        # Stage all changes
        logging.info("Staging all changes...")
        success, _ = run_git_command('git add .', repo_path)
        if success:
            # Commit changes
            logging.info("Committing changes...")
            commit_message = f"Commit by {project}"
            success, _ = run_git_command(f'git commit -m "{commit_message}"', repo_path)
            if success:
                # Push changes to the remote repository
                logging.info("Pushing changes to remote...")
                success, _ = run_git_command(f'git push -u {remote_name} {branch_name}', repo_path)
                if success:
                    logging.info("Remote repository is now in sync with local.")
                    print("Remote repository is now in sync with local.")
                    return True
                else:
                    logging.error("Failed to push changes to remote.")
                    return False
            else:
                logging.error("Failed to commit changes.")
                return False
        else:
            logging.error("Failed to stage changes.")
            return False
    else:
        logging.error("Not a git repository or failed to check status.")
        return False
    
if __name__ == "__main__":
    if sync_remote_with_local(project='test', remote_name='origin', branch_name='featurebranch'):
        print("Sync completed successfully.")
    else:
        print("An error occurred during sync.")
