import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import json

load_dotenv()

jira_url = os.getenv("JIRA_URL")
email = os.getenv("JIRA_USERNAME")
token = os.getenv("JIRA_API_TOKEN")

print(f"Testing Jira Connection...")
print(f"URL: {jira_url}")
print(f"User: {email}")

auth = HTTPBasicAuth(email, token)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Test 1: Get User (Myself) to verify auth
try:
    print("\n1. Verifying Authentication (Get Myself)...")
    me_url = f"{jira_url}/rest/api/3/myself"
    response = requests.get(me_url, headers=headers, auth=auth)
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"Success! Authenticated as: {user_data.get('displayName')} ({user_data.get('emailAddress')})")
    else:
        print(f"Failed: {response.status_code}")
        print(response.text)
        exit(1)

    print("\n4. Testing Worklog Query...")
    search_url = f"{jira_url}/rest/api/3/search/jql"
    # Exact query used in jira_client.py
    jql = "worklogAuthor = 'toshnavkhatke20@gmail.com' AND worklogDate = '2026-02-12'"
    payload = {
        "jql": jql,
        "maxResults": 5,
        "fields": ["summary", "status", "worklog"]
    }
    response = requests.post(
        search_url, 
        headers=headers, 
        auth=auth,
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        total = data.get("total", 0)
        print(f"Found {total} issues in SAM1.")
        
        for issue in data.get("issues", []):
            print(f"\nKey: {issue['key']}")
            print(f"Summary: {issue['fields']['summary']}")
            worklogs = issue['fields'].get('worklog', {}).get('worklogs', [])
            print(f"Worklogs count: {len(worklogs)}")
            for w in worklogs:
                print(f" - Author: {w.get('author', {}).get('emailAddress')}")
                print(f" - Time: {w.get('timeSpent')}")
                if "comment" in w:
                    print(f" - Comment Type: {type(w['comment'])}")
                    print(f" - Comment Content: {w['comment']}")
    else:
        print(f"Failed: {response.text}")

except Exception as e:
    print(f"Error: {e}")
