import time
import logging
from google.api_core.exceptions import ServiceUnavailable, InternalServerError, GoogleAPICallError
from app.config import settings
from app.services.gemini_client import generate

logger = logging.getLogger(__name__)

def generate_workout_gemini(name, age, weight, goal, intensity):
    prompt = f"""Create a safe personalized 7-day workout plan for {name}, age {age}, weight {weight}kg, goal {goal}, intensity {intensity}. For each day give focus, warm-up, exercises with sets/reps or duration, rest and cool-down. Include recovery where appropriate. Avoid dangerous/extreme/medical advice. Return only the plan."""
    
    primary_model = settings.GEMINI_WORKOUT_MODEL
    fallback_model = "gemini-1.5-flash"
    max_retries = 3

    # 1st attempt: Try primary model with exponential backoff
    for attempt in range(max_retries):
        try:
            return generate(prompt, primary_model)
        except (ServiceUnavailable, InternalServerError) as e:
            wait_time = (2 ** attempt) + 1  # Waits 2s, 3s, 5s
            logger.warning(
                f"Primary model '{primary_model}' temporary failure (Attempt {attempt + 1}/{max_retries}): {e}. Retrying in {wait_time}s..."
            )
            time.sleep(wait_time)
        except GoogleAPICallError as e:
            # Non-transient errors (like invalid argument) shouldn't be retried blindly
            logger.error(f"Google API call error with primary model: {e}")
            break

    # 2nd attempt: Fallback model execution
    logger.info(f"Switching to fallback model '{fallback_model}'...")
    try:
        return generate(prompt, fallback_model)
    except Exception as e:
        logger.error(f"Fallback model also failed: {e}")
        raise Exception("Gemini API is currently overloaded. Please try again in 1 minute.") from e