import requests
import json

def analyze_email(subject, body):

    prompt = f"""
You are an email assistant for a B.Tech CSE student.

Return ONLY valid JSON.

Rules:

INTERNSHIP
- internships
- placements
- hackathons
- coding contests
- career opportunities

ACADEMIC
- project invitations
- library notices
- course notices
- academic announcements

MESS
- mess menus
- food notices

EVENT
- sports
- yoga
- celebrations
- workshops
- seminars
- club activities

IGNORE
- advertisements
- shopping promotions
- MTech admissions
- PhD admissions
- faculty recruitment

Priority Rules:
INTERNSHIP -> HIGH
ACADEMIC -> MEDIUM
EVENT -> MEDIUM
MESS -> LOW
IGNORE -> LOW

Relevance Rules:
INTERNSHIP -> 9
ACADEMIC -> 7
EVENT -> 5
MESS -> 1
IGNORE -> 0

Summary Rules:
Generate exactly one sentence.
For MESS emails:
deadline = NONE
Deadline Rules:
Extract deadline if present.
Otherwise return NONE.

Email Subject:
{subject}

Email Body:
{body}

Return EXACTLY:

{{
  "category":"",
  "priority":"",
  "summary":"",
  "deadline":"",
  "relevance":0
}}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
    )

    data = response.json()

    print("OLLAMA RESPONSE:")

    if "response" not in data:
        raise Exception(f"Ollama Error: {data}")

    return json.loads(data["response"])