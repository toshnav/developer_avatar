from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
import os
from models import ActivitySummary

def summarize_activity(jira_data: dict) -> ActivitySummary:
    """
    Uses LangChain to summarize the daily activity fetched from Jira.
    """
    llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()
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

    # Construct the prompt
    issues_text = ""
    for issue in jira_data.get("issues", []):
        issues_text += f"- {issue['key']}: {issue['summary']} ({issue['status']})\n"
        issues_text += f"  Time: {issue['time_spent_seconds']/3600:.2f} hours\n"
        if issue.get("comments"):
            issues_text += f"  Comments: {', '.join(issue['comments'])}\n"
    
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
