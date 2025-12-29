import os
import time
from dotenv import load_dotenv
from groq import Groq, RateLimitError, APIConnectionError, APIError

load_dotenv()
API_KEY = os.environ.get("GROQ_API_KEY")

client = None
if API_KEY:
    client = Groq(api_key=API_KEY)

MODEL_NAME = "llama-3.1-8b-instant"

# MODIFICATION 1: System Instruction to enforce relevance
SYSTEM_INSTRUCTION = """
You are a specialized AI assistant for a Diabetes Health platform. 
Your role is to answer questions ONLY related to:
1. Diabetes management and education
2. General Health and Wellness
3. Diet, Nutrition, and Food
4. Exercise and Fitness
5. Lifestyle changes for better health
6. Exchange of Greetings

CRITICAL RULES:
- If the user asks about ANYTHING else (e.g., coding, movies, politics, general knowledge, math, history), you MUST refuse.
- If you refuse, your output must be EXACTLY this sentence: "I am your health assistant. Please ask a question related to diabetes, diet, or exercise."
- Do NOT prescribe specific medications (insulin dosages, pill names). You are not a doctor.
"""

def get_llama_response(prompt, max_retries=3):
    if not client:
        return {"status": "error", "payload": "Server configuration error: Missing API Key."}

    # Combine System Instruction with User Prompt
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTION},
        {"role": "user", "content": prompt}
    ]
    
    retries = 0
    while retries < max_retries:
        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.5, # Lower temperature for stricter adherence
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            
            return {
                "status": "success", 
                "payload": completion.choices[0].message.content
            }

        except RateLimitError:
            wait_time = (2 ** retries) + 1  
            time.sleep(wait_time)
            retries += 1

        except APIConnectionError:
            time.sleep(2)
            retries += 1     
        
        except APIError as e:
            return {"status": "error", "payload": f"Groq API Error: {str(e)}"}
            
        except Exception as e:
            return {"status": "error", "payload": f"An unexpected error occurred: {str(e)}"}
            
    return {"status": "error", "payload": "Max retries exceeded. Please try again later."}