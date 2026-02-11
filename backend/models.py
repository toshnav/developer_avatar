from pydantic import BaseModel
from typing import List, Optional

class DailyActivityRequest(BaseModel):
    developer_email: str
    date: str  # YYYY-MM-DD

class ActivitySummary(BaseModel):
    total_hours: float
    issues_worked_on: List[str]
    summary: str
    status: str

class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None
