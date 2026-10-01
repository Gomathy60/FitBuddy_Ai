# FitBuddy

## VS Code / Windows
1. `python -m venv .venv`
2. `.venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your Gemini API key.
5. `uvicorn app.main:app --reload`
6. Open http://127.0.0.1:8000
7. API docs: http://127.0.0.1:8000/docs
8. Admin: http://127.0.0.1:8000/admin?key=fitbuddy-admin-123
9. Tests: `pytest -q`
