from pydantic import BaseModel
from typing import List, Optional

class DailyActivityRequest(BaseModel):
    developer_email: str
    date: str  # YYYY-MM-DD
    llm_provider: str = "azure"

class IssueDetail(BaseModel):
    key: str
    summary: str
    status: str
    time_spent: float
    comments: List[str]

class ActivitySummary(BaseModel):
    total_hours: float
    issues_worked_on: List[str]
    details: List[IssueDetail] = []
    summary: str
    status: str

class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None

class TimesheetEntry(BaseModel):
    date: str
    project: str
    task: str
    task_description: str
    status: str
    remark: str
    hours: str
    billable: str
    role: str
    site: str

class TimesheetRequest(BaseModel):
    jira_email: str
    jira_project_key: str
    github_username: str
    github_token: Optional[str] = None
    days: int = 5
    employee_id: str
    employee_name: str
    billable: str = "Yes"
    role: str = "Developer"
    site: str = "Offshore"
    authorized_hours: str = "8"
    llm_provider: str = "azure"
