
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"


from database import get_db_connection
import psycopg2.extras

def get_user_profile():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT keyword, score FROM user_interests ORDER BY score DESC LIMIT 15")
            rows = cursor.fetchall()
            if not rows:
                return "No interaction profile available. Rely on standard B.Tech CSE priorities."
            
            profile = "USER INTERACTION PROFILE (Higher score = higher relevance):\n"
            for row in rows:
                profile += f"- {row[0]}: {row[1]}\n"
            return profile
    except:
        return "No interaction profile available."

def analyze_email(subject, body):
    user_profile = get_user_profile()

    prompt = f"""
You are an advanced email intelligence agent for a B.Tech CSE student.
Your goal is to accurately classify and grade the relevance of incoming emails.

Return ONLY valid JSON.

USER PROFILE:
The user actively interacts with emails containing the following themes:
{user_profile}

Categories:
INTERNSHIP - placements, jobs, hackathons
ACADEMIC - courses, library, projects
MESS - food notices, mess menus
EVENT - sports, celebrations, seminars
PHD_SEMINAR - PhD seminars, viva-voce, PhD presentations
IGNORE - spam, generic advertisements

Relevance Scoring Rules (1-10):
- Must be an integer exactly between 1 and 10.
- Do NOT use static scores. Grade dynamically based on the email content.
- Base your score heavily on the USER PROFILE provided above. If an email matches high-scoring keywords, bump its relevance.
- 9-10: Highly personalized, urgent action required, or matches top user interests.
- 6-8: Important general notices, upcoming events matching user interests.
- 3-5: Generic university blasts, low-priority events.
- 1-2: Spam, generic advertisements, or topics the user ignores.

Priority Rules (LOW, MEDIUM, HIGH, CRITICAL):
- Strictly map priorities in this exact hierarchy if applicable: INTERNSHIP > ACADEMIC > EVENT > MESS.
- CRITICAL: Internship emails with deadlines, or highly urgent Academic items.
- HIGH: General Internship emails, or Academic emails.
- MEDIUM: Event emails.
- LOW: Mess emails or IGNORE category.
- PhD Seminars should be LOW priority as they will be filtered away anyway.

Summary Rules:
- Generate a natural, conversational 2-3 sentence brief summarizing the core intent of the email.
- Write it in the second-person ("You have received...", "This email is about...").
- Keep it highly readable and engaging. Do NOT use bullet points or strict lists.

Adaptive Action Rules:
- Analyze the user's historical profile and the email's relevance.
- Choose exactly ONE adaptive action: ARCHIVE, STAR, MARK_READ, or NONE.
- Use ARCHIVE if the email is a low-priority generic advertisement or irrelevant.
- Use STAR if it is highly relevant, urgent, or matches the user's top interests.
- Use MARK_READ for unimportant notices.
- Use NONE for standard processing.

Deadline Rules:
Extract deadline if present. Return ONLY in YYYY-MM-DD format (e.g., 2026-06-08). If no deadline exists, return: NONE

Email Subject:
{subject}

Email Body:
{body}

Return ONLY:
{{
  "category":"",
  "tags":[],
  "priority":"",
  "summary":"",
  "deadline":"",
  "relevance":0,
  "adaptive_action":""
}}
"""

    try:
        import os
        from groq import Groq
        
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that returns JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        result_text = completion.choices[0].message.content
        result = json.loads(result_text)

        required_keys = [
            "category",
            "priority",
            "summary",
            "deadline",
            "relevance",
            "adaptive_action"
        ]

        for key in required_keys:
            if key not in result:
                raise Exception(f"Missing key: {key}")

        print("GROQ RESPONSE:")
        return result

    except Exception as e:
        print(f"Groq Error: {e}")
        if "429" in str(e) or "rate" in str(e).lower():
            raise Exception("RATE_LIMIT")
            
        return {
            "category": "ERROR",
            "priority": "LOW",
            "summary": f"AI Error: {str(e)}",
            "deadline": "NONE",
            "relevance": 0,
            "adaptive_action": "NONE"
        }
