import os
from dotenv import load_dotenv
import requests
from plyer import notification
import time
from datetime import datetime, timedelta, timezone

# Load environment variables from the .env file
load_dotenv()

def get_github_activity(owner, repo):
    base_url = f"https://api.github.com/repos/{owner}/{repo}/events"
    response = requests.get(base_url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_seen_event_ids():
    # Load seen event IDs from a file
    seen_event_ids_file = "seen_event_ids.txt"
    if os.path.exists(seen_event_ids_file):
        with open(seen_event_ids_file, "r") as file:
            return set(file.read().splitlines())
    else:
        return set()


def notify_activity(owner, repo):
    activity = get_github_activity(owner, repo)

    if activity:
        for event in activity:    
            created_at = event['created_at']
            event_timestamp = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

            # Only show notifications for events that occurred after the current time minus a specific duration (e.g., 1 hour)
            if event_timestamp > datetime.now(timezone.utc) - timedelta(hours=1):
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


def get_user_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        repositories = response.json()
        return [repo['name'] for repo in repositories]
    else:
        return None
    

def main():
    # Retrieve GitHub usernames and repositories from environment variables
    github_username = os.getenv("GITHUB_USERNAME")
    repositories = get_user_repositories(github_username)


    while True:
        for repo in repositories:
            notify_activity(github_username, repo)

        # Check for updates every 5 minutes (adjust as needed)
        time.sleep(300)

if __name__ == "__main__":
    main()
