from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import DailyActivityRequest, ActivitySummary, ChatRequest
from jira_client import get_developer_activity
from agent import summarize_activity
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
        summary = summarize_activity(jira_data)
        
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
