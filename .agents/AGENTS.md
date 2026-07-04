# Omnichannel Uniformity Rule
Whenever the user requests a feature addition, UI change, or modification to the "agent application", you MUST evaluate and apply the change across ALL platforms to ensure strict uniformity:
1. **Web App** (React/Vite in `frontend/`)
2. **Mobile App** (Flutter in `mobile_app/`)
3. **Desktop App** (If applicable, or Electron wrapper)
4. **Backend API** (FastAPI in `api.py` and background scripts)

Do not assume a feature request only applies to the web dashboard. Ensure the same data models, UI paradigms, and logic are reflected in the Flutter mobile application as well.
