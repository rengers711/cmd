import time
import requests
import os

# Get GitHub token securely from environment variables
GITHUB_TOKEN = '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'  # Replace this with your actual GitHub token

# List of repositories and their workflow run IDs
workflows = [
    {'owner': 'tmhcs12', 'repo': 'sc71-73', 'run_id': '12118305709'},
    {'owner': 'tmhcs12', 'repo': 'sc4-4ff', 'run_id': '12118276797'},
    {'owner': 'tmhcs12', 'repo': 'sc5-5f', 'run_id': '12118822326'},
    {'owner': 'tmhcs12', 'repo': 'sc6-6f', 'run_id': '12119843177'},
    {'owner': 'tmhcs12', 'repo': 'sc7-7f', 'run_id': '12120145468'}
]

# Function to re-run a workflow
def rerun_workflow(owner, repo, run_id):
    github_api_url = f'https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/rerun'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
    }

    response = requests.post(github_api_url, headers=headers)

    if response.status_code == 201:
        print(f"Workflow run {run_id} for repository {repo} re-triggered successfully!")
    elif response.status_code == 204:
        print(f"Workflow run {run_id} for repository {repo} re-triggered successfully, but no content returned.")
    elif response.status_code == 401:
        print(f"Failed to re-run workflow {run_id} for repository {repo}. Status code: 401")
        print("Possible reasons: Invalid or expired token, or insufficient permissions.")
    else:
        try:
            response_json = response.json()
            print(f"Failed to re-run workflow {run_id} for repository {repo}. Status code: {response.status_code}")
            print("Response:", response_json)
        except ValueError:
            print(f"Failed to re-run workflow {run_id} for repository {repo}. Status code: {response.status_code}")
            print("No additional response content available.")

# Run the script every 6 hours (21600 seconds)
while True:
    for workflow in workflows:
        try:
            rerun_workflow(workflow['owner'], workflow['repo'], workflow['run_id'])
        except Exception as e:
            print(f"An error occurred while processing {workflow['repo']}: {e}")
    time.sleep(21600)  # 6 hours in seconds
