# Mail Agent (AI-Powered Gmail Assistant)

Mail Agent is an intelligent, multi-tenant AI email assistant designed to seamlessly sync your inbox across all platforms. It autonomously reads, categorizes, grades, and summarizes your emails using advanced Large Language Models, ensuring you never miss a deadline or an important update.

## 🚀 Features

- **Omnichannel Syncing**: Works perfectly across the React Web Dashboard, Tauri Desktop App, and Flutter Mobile App.
- **AI Brief Summaries**: Replaces long emails with concise, actionable summaries using Groq's blazing-fast `llama-3.3-70b-versatile` model.
- **Deadline Tracking**: Automatically detects deadlines in emails (e.g., hackathons, assignments) and sorts them by urgency so the most pressing items are always at the top of your inbox.
- **Smart Categorization & Labels**: Automatically categorizes emails into predefined buckets (Internship, Academic, Event, Mess, etc.) and allows for dynamic, adaptive labeling based on your interests.
- **Google Calendar Integration**: Automatically extracts events and deadlines and syncs them directly to your Google Calendar.
- **Relevance & Importance Scoring**: Dynamically grades incoming emails on a 1-10 scale based on your personalized user profile.

## 💻 Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL (Supabase)
- **AI / LLM**: Groq API (`llama-3.3-70b-versatile`)
- **Web / Desktop Frontend**: React + Vite + Tauri + TailwindCSS
- **Mobile Frontend**: Flutter

## 🛠️ Recent Updates

1. **Omnichannel UI Alignment**: The web login UI has been fully redesigned to exactly match the deep dark aesthetic and glassmorphic elements of the Flutter mobile app.
2. **Deadline UI & Sorting**: Deadlines now have their own dedicated UI section across all platforms and are used to sort your labels dynamically.
3. **Model Upgrade**: Switched the AI brain from Llama 3 8B to the highly capable Llama 3.3 70B for near-flawless reasoning and JSON parsing.
4. **Cloud Deployment**: The React frontend is now statically served directly from the FastAPI backend, allowing the entire web dashboard to be natively hosted on a single Render URL.

## ⚙️ Running Locally

1. **Backend**:
   Ensure you have your `.env` configured with your Supabase URL, Groq API Key, and Google OAuth credentials.
   ```bash
   call venv\Scripts\activate.bat
   python main.py
   ```
   Or use the hidden background script: `run_backend_hidden.vbs`

2. **Web App**:
   ```bash
   cd frontend
   npm run dev
   ```
