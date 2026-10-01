from app.config import settings
from app.services.gemini_client import generate
def generate_nutrition_tip_with_flash(goal,age,weight):
 return generate(f"Give one concise healthy nutrition or recovery tip for age {age}, weight {weight}kg and goal {goal}. No extreme dieting or medical advice. 2-5 sentences.",settings.GEMINI_TIP_MODEL)
