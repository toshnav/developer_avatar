import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Construct the full URL
url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"

print(f"Testing URL: {url}")

headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

data = {
    "messages": [
        {"role": "user", "content": "Hello"}
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
