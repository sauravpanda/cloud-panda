from flask import Flask, request, jsonify
import requests
import os
import time
import jwt
import json
import helpers
import r2r_client
import asyncio
app = Flask(__name__)

# GitHub App configuration
GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')
GITHUB_APP_WEBHOOK_SECRET = os.environ.get('GITHUB_APP_WEBHOOK_SECRET')

# GitHub API endpoints
GITHUB_API_BASE_URL = 'https://api.github.com'
GITHUB_APP_INSTALLATION_URL = f'{GITHUB_API_BASE_URL}/app/installations'

# Manual Installation ID

def run_async(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return wrapper

def generate_jwt():
    # Define the time the JWT was issued and its expiration time
    issued_at_time = int(time.time())
    expiration_time = issued_at_time + (7 * 60)  # JWT expires in 15 minutes

    # Define the JWT payload
    payload = {
        'iat': issued_at_time,
        'exp': expiration_time,
        'iss': GITHUB_APP_ID
    }
    print("GITHUB_APP_ID, ", GITHUB_APP_ID)
    with open(".key.pem", "r") as f:
        # Encode the JWT using the RS256 algorithm
        encoded_jwt = jwt.encode(payload, f.read(), algorithm='RS256')
    return encoded_jwt


def get_installations():
    headers = {
        'Authorization': f'Bearer {generate_jwt()}',
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }
    url = "https://api.github.com/app/installations"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_installation_access_token(installation_id, permissions=None):
    headers = {
        'Authorization': f'Bearer {generate_jwt()}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()['token']


# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.get_json()
    event = request.headers.get('X-GitHub-Event')
    print(json.dumps(payload, indent=2))
    installation_id = payload["installation"]["id"]
    if event == 'push':
        # Handle push event
        repository = payload['repository']['full_name']
        branch = payload['ref'].split('/')[-1]
        commit_message = payload['head_commit']['message']
        # Perform desired actions based on the push event data
        print(f'Received push event for repository: {repository}')
        print(f'Branch: {branch}')
        print(f'Commit message: {commit_message}')
        # Add your custom logic here

    elif event == 'pull_request':
        # Handle pull request event
        action = payload['action']
        if action == 'opened':
            pull_request_number = payload['pull_request']['number']
            # Perform desired actions based on the pull request event data
            print(f'Received pull request event with action: {action}')
            print(f'Pull request number: {pull_request_number}')
            repo_owner = payload["repository"]["owner"]["login"]
            repo_name = payload["repository"]["name"]
            pull_number = payload["pull_request"]["number"]
            print("Running code review")

            helpers.review_code(payload, get_installation_access_token(installation_id))
        
        # Add your custom logic here

    elif payload['action'] == 'created' and 'issue' in payload:
        # Extract relevant information from the payload
        repo_name = payload["repository"]["name"]
        if "R2R" in repo_name:
            helpers.reply_to_r2r_comments(payload, get_installation_access_token(installation_id))
        else:
            helpers.reply_to_comment(payload, get_installation_access_token(installation_id))
        
    # elif payload['action'] == 'opened' and 'issue' in payload:
    #     issue_number = payload['issue']['number']
    #     issue_title = payload['issue']['title']
    #     issue_body = payload['issue']['body']

    #     if "CREATE" in issue_title:
    #         helpers.create_files(payload, get_installation_access_token(installation_id))
    #     elif "DOC" in issue_title:
    #         helpers.document_code(payload, get_installation_access_token(installation_id))
    else:
        # Handle other events
        print(f'Received event: {event}')
        # Add your custom logic here

    return jsonify({'message': 'Webhook received'})


# GitHub App authentication
@app.route('/')
def hello():
    return jsonify({'message': "Hello World!!"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80")
