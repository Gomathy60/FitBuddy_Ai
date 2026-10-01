from functools import lru_cache
from google import genai
from app.config import settings
@lru_cache
def client():
 if not settings.GEMINI_API_KEY: raise RuntimeError('GEMINI_API_KEY is missing in .env')
 return genai.Client(api_key=settings.GEMINI_API_KEY)
def generate(prompt,model):
 r=client().models.generate_content(model=model,contents=prompt); t=getattr(r,'text',None)
 if not t: raise RuntimeError('Gemini returned an empty response')
 return t.strip()
