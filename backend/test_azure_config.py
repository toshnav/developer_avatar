import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

print(f"LLM_PROVIDER: {os.getenv('LLM_PROVIDER')}")
print(f"AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
print(f"AZURE_OPENAI_DEPLOYMENT_NAME: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}")
print(f"AZURE_OPENAI_API_VERSION: {os.getenv('AZURE_OPENAI_API_VERSION')}")

try:
    llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0.7
    )
    print("LLM Initialized. Invoking...")
    response = llm.invoke([HumanMessage(content="Hello")])
    print(f"Response: {response.content}")
except Exception as e:
    print(f"Error: {e}")
