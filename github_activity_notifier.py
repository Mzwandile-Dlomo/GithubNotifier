import os
from dotenv import load_dotenv
import requests
from plyer import notification
import time

# Load environment variables from the .env file
load_dotenv()

def get_github_activity(owner, repo):
    base_url = f"https://api.github.com/repos/{owner}/{repo}/events"
    response = requests.get(base_url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def notify_activity(owner, repo):
    activity = get_github_activity(owner, repo)

    if activity:
        for event in activity:
            if event['type'] in ['IssuesEvent', 'PullRequestEvent', 'ReleaseEvent']:
                title = f"New {event['type']} in {owner}/{repo}"
                description = event['payload']['action'] if 'action' in event['payload'] else 'New Activity'
                body = f"Description: {description}\n\n"
                
                if 'issue' in event['payload']:
                    body += f"Issue Title: {event['payload']['issue']['title']}\n"
                    body += f"Issue URL: {event['payload']['issue']['html_url']}\n"
                
                if 'pull_request' in event['payload']:
                    body += f"Pull Request Title: {event['payload']['pull_request']['title']}\n"
                    body += f"Pull Request URL: {event['payload']['pull_request']['html_url']}\n"
                
                if 'release' in event['payload']:
                    body += f"Release Name: {event['payload']['release']['name']}\n"
                    body += f"Release URL: {event['payload']['release']['html_url']}\n"

                notification.notify(
                    title=title,
                    message=body,
                    app_icon=None,
                    timeout=10,
                )

def main():
    # Retrieve GitHub usernames and repositories from environment variables
    usernames = os.getenv("GITHUB_USERNAME").split(',')
    repositories = os.getenv("GITHUB_REPOS").split(',')

    while True:
        for owner, repo in zip(usernames, repositories):
            notify_activity(owner, repo)

        # Check for updates every 10 minutes (adjust as needed)
        time.sleep(600)

if __name__ == "__main__":
    main()
