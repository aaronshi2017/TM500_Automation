import requests

# Jenkins server details
jenkins_url = 'http://localhost:8070'
job_name = 'Test_TM500_Pipeline_Github'
username = 'admin'
api_token = '118bb2769a9aeedcd3947ae37350c89543'

# Construct the URL
trigger_url = f"{jenkins_url}/job/{job_name}/build"

# Make the POST request to trigger the job
response = requests.post(trigger_url, auth=(username, api_token))

# Check the response
if response.status_code == 201:
    print('Job triggered successfully')
else:
    print(f'Failed to trigger job: {response.status_code}, {response.text}')
