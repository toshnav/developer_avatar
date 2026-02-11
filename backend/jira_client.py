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

def _extract_text_from_adf(node):
    """
    Recursively extracts text from an Atlassian Document Format (ADF) node.
    """
    if isinstance(node, dict):
        if "text" in node:
            return node["text"]
        if "content" in node:
            return " ".join([_extract_text_from_adf(child) for child in node["content"]])
    elif isinstance(node, list):
         return " ".join([_extract_text_from_adf(child) for child in node])
    return ""

def get_developer_activity(email: str, date: str):
    """
    Fetches activity for a developer on a specific date.
    Returns a dictionary with worklogs, issues, and comments.
    """
    jira_url = os.getenv("JIRA_URL")
    if not jira_url:
        return {"error": "JIRA_URL not set"}
    
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
        
        time_spent_seconds = 0
        comments = []
        
        for worklog in worklogs:
             # Basic check, date format from Jira is usually ISO 8601
             if date in worklog.get("started", "") and worklog.get("author", {}).get("emailAddress") == email:
                 time_spent_seconds += worklog.get("timeSpentSeconds", 0)
                 if "comment" in worklog and worklog["comment"]:
                     # Extract text from ADF or string
                     if isinstance(worklog["comment"], dict):
                         text = _extract_text_from_adf(worklog["comment"])
                         if text.strip():
                            comments.append(text)
                     elif isinstance(worklog["comment"], str):
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
