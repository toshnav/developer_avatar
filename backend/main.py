from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import DailyActivityRequest, ActivitySummary, ChatRequest, TimesheetRequest, TimesheetEntry
from jira_client import get_developer_activity
from agent import summarize_activity, generate_timesheet_entry
from github_client import GitHubClient
from datetime import datetime, timedelta
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Autum - Developer Avatar API")

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Autum API"}

@app.post("/activity/summary", response_model=ActivitySummary)
async def get_activity_summary(request: DailyActivityRequest):
    try:
        # Fetch data from Jira
        jira_data = get_developer_activity(request.developer_email, request.date)
        
        # Process with LangChain Agent
        summary = summarize_activity(jira_data, request.llm_provider)
        
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/timesheet/generate", response_model=List[TimesheetEntry])
async def generate_timesheet(request: TimesheetRequest):
    try:
        # Calculate dates
        dates = []
        today = datetime.now()
        for i in range(request.days):
            date_obj = today - timedelta(days=i)
            # Skip defaults if needed, but for now simple range
            dates.append(date_obj.strftime("%Y-%m-%d"))
        
        # Initialize GitHub Client
        gh_client = GitHubClient(token=request.github_token or os.getenv("GITHUB_TOKEN"))
        
        results = []
        for date in dates:
            # 1. Fetch Jira Data
            jira_data = get_developer_activity(request.jira_email, date)
            if "error" in jira_data:
                jira_data = {} # Handle gracefully
            
            # 2. Fetch GitHub Data
            github_data = await gh_client.get_activity(request.github_username, date)
            if github_data and "error" in github_data[0]:
                github_data = [] # Handle gracefully
            
            # 3. Generate Entry
            config = {
                "jira_project_key": request.jira_project_key,
                "billable": request.billable,
                "role": request.role,
                "site": request.site,
                "authorized_hours": request.authorized_hours
            }
            
            entry = generate_timesheet_entry(jira_data, github_data, date, config, request.llm_provider)
            results.append(entry)
            
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
