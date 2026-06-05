import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": "Summarize: Groww is hiring interns. Deadline June 15.",
        "stream": False
    }
)

print(response.json()["response"])