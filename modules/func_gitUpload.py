import os
import subprocess

def run_command(command, cwd=None):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        raise subprocess.CalledProcessError(result.returncode, command)
    return result.stdout

def is_git_repository(path):
    """Check if a given directory is a git repository."""
    try:
        run_command('git status', cwd=path)
        return True
    except subprocess.CalledProcessError:
        return False

def sync_remote_with_local(local_repo_path, project='test', remote_name='origin', branch_name='newbranch'):

    if not is_git_repository(local_repo_path):
        raise Exception(f"The directory {local_repo_path} is not a git repository.")

    # Stage all changes
    print("Staging all changes...")
    run_command('git add .', cwd=local_repo_path)

    # Commit changes
    print("Committing changes...")
    commit_message = f"Commit by {project}"
    run_command(f'git commit -m "{commit_message}"', cwd=local_repo_path)

    # Push changes to the remote repository
    print("Pushing changes to remote...")
    run_command(f'git push -u {remote_name} {branch_name}', cwd=local_repo_path)

    print("Remote repository is now in sync with local.")

# Usage
local_repo_path = '.'  # Change this to your local repository path

try:
    sync_remote_with_local(local_repo_path)
    print("Sync completed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
