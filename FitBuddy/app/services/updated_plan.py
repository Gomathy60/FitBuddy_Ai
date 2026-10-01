from app.config import settings
from app.services.gemini_client import generate
def update_workout_plan(original_plan,feedback,name,goal,intensity):
 return generate(f"""Revise this 7-day workout plan using the feedback. Original:
{original_plan}
User: {name}, goal: {goal}, intensity: {intensity}
Feedback: {feedback}
Return exactly 7 days. Each day: focus, warm-up, workout, sets/reps or duration, rest, recovery. Keep it safe and practical. Return only revised plan.""",settings.GEMINI_WORKOUT_MODEL)
