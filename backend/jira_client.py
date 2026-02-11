import requests
from requests.auth import HTTPBasicAuth
import os
import json
from datetime import datetime

def get_jira_headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

def get_jira_auth():
    email = os.getenv("JIRA_USERNAME")
    token = os.getenv("JIRA_API_TOKEN")
    return HTTPBasicAuth(email, token)

def get_developer_activity(email: str, date: str):
    """
    Fetches activity for a developer on a specific date.
    Returns a dictionary with worklogs, issues, and comments.
    """
    jira_url = os.getenv("JIRA_URL")
    if not jira_url:
        return {"error": "JIRA_URL not set"}

    # This is a simplified example. In a real scenario, we might need to search for user accountId first.
    # For now, let's assume we can search issues assigned to the user or worklogs by the user.
    
    # 1. Search for issues updated by the user on that date
    jql = f"worklogAuthor = '{email}' AND worklogDate = '{date}'"
    search_url = f"{jira_url}/rest/api/3/search/jql"
    
    payload = {
        "jql": jql,
        "fields": ["summary", "status", "worklog"]
    }

    response = requests.post(
        search_url,
        headers=get_jira_headers(),
        auth=get_jira_auth(),
        json=payload
    )
    
    if response.status_code != 200:
        return {"error": f"Failed to fetch Jira data: {response.text}"}
        
    issues = response.json().get("issues", [])
    
    activity_data = {
        "date": date,
        "developer": email,
        "issues": [],
        "total_time_seconds": 0
    }
    
    for issue in issues:
        issue_summary = issue["fields"]["summary"]
        issue_status = issue["fields"]["status"]["name"]
        
        # Filter worklogs for the specific user and date
        worklogs = issue["fields"].get("worklog", {}).get("worklogs", [])
        # If worklogs are not fully expanded, we might need to fetch them separately.
        # For MVP, assuming they are present or we iterate.
        
        time_spent_seconds = 0
        comments = []
        
        for worklog in worklogs:
             # Basic check, date format from Jira is usually ISO 8601
             if date in worklog.get("started", "") and worklog.get("author", {}).get("emailAddress") == email:
                 time_spent_seconds += worklog.get("timeSpentSeconds", 0)
                 if "comment" in worklog and worklog["comment"]:
                     # Extract comment text (simplified)
                     comments.append(worklog["comment"])

        if time_spent_seconds > 0:
            activity_data["issues"].append({
                "key": issue["key"],
                "summary": issue_summary,
                "status": issue_status,
                "time_spent_seconds": time_spent_seconds,
                "comments": comments
            })
            activity_data["total_time_seconds"] += time_spent_seconds
            
    return activity_data
