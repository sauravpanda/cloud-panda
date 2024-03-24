from flask import Flask, request, jsonify
import requests
import os
import time
import jwt

app = Flask(__name__)

# GitHub App configuration
GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')
GITHUB_APP_WEBHOOK_SECRET = os.environ.get('GITHUB_APP_WEBHOOK_SECRET')

# GitHub API endpoints
GITHUB_API_BASE_URL = 'https://api.github.com'
GITHUB_APP_INSTALLATION_URL = f'{GITHUB_API_BASE_URL}/app/installations'

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


def get_installation_access_token(installation_id, permissions):
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
        pull_request_number = payload['pull_request']['number']
        # Perform desired actions based on the pull request event data
        print(f'Received pull request event with action: {action}')
        print(f'Pull request number: {pull_request_number}')
        # Add your custom logic here

    else:
        # Handle other events
        print(f'Received event: {event}')
        # Add your custom logic here

    return jsonify({'message': 'Webhook received'})


# GitHub App authentication
@app.route('/repos')
def github_app_auth():
    access_token = get_installations()
    return jsonify({'access_token': access_token})




if __name__ == '__main__':
    app.run()