from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
import os
from models import ActivitySummary, TimesheetEntry, IssueDetail

def summarize_activity(jira_data: dict, llm_provider: str = None) -> ActivitySummary:
    """
    Uses LangChain to summarize the daily activity fetched from Jira.
    """
    llm_provider = (llm_provider or os.getenv("LLM_PROVIDER", "openai")).lower()
    llm = None

    if llm_provider == "azure":
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

        if not api_key or not endpoint:
             return _mock_summary(jira_data, "Azure OpenAI credentials not set.")
        
        llm = AzureChatOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            azure_deployment=deployment,
            api_version=api_version,
            temperature=0.7
        )

    elif llm_provider == "grok":
        api_key = os.getenv("GROK_API_KEY")
        if not api_key:
             return _mock_summary(jira_data, "Grok API Key not set.")
        
        # Grok is compatible with OpenAI's API structure
        llm = ChatOpenAI(
            openai_api_key=api_key,
            openai_api_base="https://api.x.ai/v1",
            model_name="grok-4-latest",
            temperature=0.7
        )
    
    elif llm_provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return _mock_summary(jira_data, "OpenAI API Key not set.")
        
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", openai_api_key=api_key)
        
    else:
        return _mock_summary(jira_data, f"Unsupported LLM Provider: {llm_provider}")

    # Construct the prompt and details
    issues_text = ""
    details = []
    
    for issue in jira_data.get("issues", []):
        issues_text += f"- {issue['key']}: {issue['summary']} ({issue['status']})\n"
        hours = issue['time_spent_seconds']/3600
        issues_text += f"  Time: {hours:.2f} hours\n"
        
        comments = issue.get("comments", [])
        if comments:
            issues_text += f"  Comments: {', '.join(comments)}\n"
            
        details.append(IssueDetail(
            key=issue['key'],
            summary=issue['summary'],
            status=issue['status'],
            time_spent=round(hours, 2),
            comments=comments
        ))
    
    total_hours = jira_data.get("total_time_seconds", 0) / 3600
    
    prompt = f"""
    You are an AI assistant representing a software developer.
    Based on the following Jira activity for today, write a daily standup summary.
    
    Total Hours: {total_hours:.2f}
    
    Activity:
    {issues_text}
    
    Please structure your response as follows:
    1.  **Work Log Breakdown**: List each issue/feature we worked on. For each, explicitly state the **Time Spent** and summarize the **Comments/Work Details**.
    2.  **Overall Summary**: A concise, first-person narrative paragraph summarizing the day's main achievements and progress (e.g., "Today I focused on...").
    
    Determine the overall status (e.g., On Track, Blocked, Completed) based on the context.
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content
        
        # Simple extraction for status
        status = "On Track"
        if "blocked" in content.lower():
            status = "Blocked"
            
        return ActivitySummary(
            total_hours=total_hours,
            issues_worked_on=[i["summary"] for i in jira_data.get("issues", [])],
            details=details,
            summary=content,
            status=status
        )
    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg:
             return _mock_summary(jira_data, f"Access Denied (403) from {llm_provider}. Check firewall/network settings.")
        if "credits" in error_msg.lower():
             return _mock_summary(jira_data, "Insufficient credits. Please check your provider's billing.")
        return _mock_summary(jira_data, f"LLM Error ({llm_provider}): {error_msg}")

def _mock_summary(jira_data: dict, message: str) -> ActivitySummary:
    return ActivitySummary(
        total_hours=jira_data.get("total_time_seconds", 0) / 3600,
        issues_worked_on=[i["summary"] for i in jira_data.get("issues", [])],
        summary=f"{message} Mock summary.",
        status="Unknown"
    )

def generate_timesheet_entry(jira_data: dict, github_data: list, date: str, config: dict, llm_provider: str = None) -> TimesheetEntry:
    """
    Generates a single timesheet entry for the day by prioritizing activities
    and using LLM to generate a remark.
    """
    # 1. Select Best Task
    selected_jira = None
    if jira_data.get("issues"):
        # Prioritize: Done/Completed > In Progress > Others
        def get_priority(issue):
            status = issue.get("status", "").lower()
            if status in ["done", "completed", "verified", "closed", "resolved"]:
                return 0
            elif status == "in progress":
                return 1
            else:
                return 2
        
        sorted_issues = sorted(jira_data["issues"], key=get_priority)
        selected_jira = sorted_issues[0]

    # 2. Prepare Context for LLM
    jira_context = ""
    if selected_jira:
        jira_context = f"Task: {selected_jira['key']} - {selected_jira['summary']}\nStatus: {selected_jira['status']}\n"
        if selected_jira.get("comments"):
            jira_context += f"Comments: {'; '.join(selected_jira['comments'])}\n"
    
    github_context = ""
    if github_data:
        github_context = "GitHub Activity:\n"
        for item in github_data[:10]: # Limit to top 10 events to avoid token limits
            if item.get("type") == "Commit":
                 github_context += f"- Commit in {item.get('repo')}: {item.get('summary')}\n"
            elif item.get("type") == "PullRequestEvent":
                 github_context += f"- PR {item.get('action')} in {item.get('repo')}: {item.get('summary')}\n"
            elif item.get("type") == "CreateEvent":
                 github_context += f"- {item.get('description')}\n"
    
    if not jira_context and not github_context:
         return TimesheetEntry(
            date=date,
            project="N/A",
            task="No Activity",
            task_description="-",
            status="-",
            remark="No activity recorded for this day.",
            hours="0",
            billable=config.get("billable", "No"),
            role=config.get("role", "Developer"),
            site=config.get("site", "Offshore")
        )

    # 3. Generate Summary via LLM
    llm_provider = (llm_provider or os.getenv("LLM_PROVIDER", "openai")).lower()
    llm = None
    
    if llm_provider == "azure":
        llm = AzureChatOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            temperature=0.7
        )
    else:
         llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")

    prompt = f"""
    You are an AI assistant generating a timesheet remark for a software developer.
    
    Date: {date}
    
    Jira Activity (Priority):
    {jira_context}
    
    GitHub Activity:
    {github_context}
    
    Task: Write a professional, concise "Remark" for the timesheet (max 2 sentences).
    - If Jira activity exists, focus on that task.
    - If only GitHub activity exists, summarize the development work.
    - Use corporate language (e.g., "Worked on...", "Implemented...", "Fixed...").
    """
    
    remark = "Generated summary."
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        remark = response.content.strip()
    except Exception as e:
        remark = f"Auto-generation failed: {str(e)[:50]}..."

    # 4. Construct Entry
    project = config.get("jira_project_key", "PROJ")
    task_summary = "General Development"
    task_desc = "See remarks"
    status = "Completed"
    
    if selected_jira:
        project = selected_jira.get("project", project) # If we captured project name in jira_client
        task_summary = selected_jira.get("summary")
        task_desc = selected_jira.get("summary")
        status = selected_jira.get("status")
    elif github_data:
        project = "Internal/GitHub"
    
    return TimesheetEntry(
        date=date,
        project=project,
        task=task_summary,
        task_description=task_desc,
        status=status,
        remark=remark,
        hours=config.get("authorized_hours", "8"),
        billable=config.get("billable", "Yes"),
        role=config.get("role", "Developer"),
        site=config.get("site", "Offshore")
    )
