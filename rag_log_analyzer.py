import os
import argparse
import json
import requests

def read_logs(log_dir):
    """Read all log files and combine them into a single string."""
    logs = []
    for root, _, files in os.walk(log_dir):
        for file in files:
            if file.endswith(".log"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    logs.append(f.read())
    return "\n".join(logs)

def send_to_llm(log_text, api_key):
    """Send log content to Google Gemini LLM and get analysis."""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Analyze the following Jenkins build logs and summarize pass/fail alerts:\n{log_text}"
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()

def extract_alerts(llm_response):
    """Extract and print the alert from the LLM response."""
    try:
        text_parts = llm_response['results'][0]['content'][0]['text']
        print("\n===== LLM Alert =====\n")
        print(text_parts)
        print("\n=====================\n")
    except Exception as e:
        print("Failed to parse LLM response:", e)

def main():
    parser = argparse.ArgumentParser(description="Analyze Jenkins logs with Google Gemini LLM")
    parser.add_argument("--log_dir", required=True, help="Directory containing log files")
    parser.add_argument("--api_key", required=True, help="Google Gemini API key")
    args = parser.parse_args()

    logs = read_logs(args.log_dir)
    if not logs.strip():
        print("No logs found to analyze.")
        return

    llm_response = send_to_llm(logs, args.api_key)
    extract_alerts(llm_response)

if __name__ == "__main__":
    main()
