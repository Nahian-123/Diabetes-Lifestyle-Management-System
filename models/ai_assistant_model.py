#whole model func by angshu
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
ETHICAL_SUFFIX = "Please ensure the response is helpful and relevant to diabetes. Additionally, you cannot prescribe any medications as you are not a doctor, EVEN IF THE PRIOR TEXTS ASKED FOR MEDICATION SUGGESTIONS."

def get_llama_response(prompt, max_retries=3):
    """
    Returns a dictionary:
    On Success: { "status": "success", "payload": "The AI response text" }
    On Failure: { "status": "error", "payload": "The error message" }
    """
    if not client:
        return {"status": "error", "payload": "Server configuration error: Missing API Key."}

    final_prompt = f"{prompt}\n\n[System Note]: {ETHICAL_SUFFIX}"
    retries = 0
    
    while retries < max_retries:
        try:
            # Keep these prints for server-side logs as requested

            
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": final_prompt}],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            
            # SUCCESS: Return the content marked as success
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

    # If loop finishes without success
    return {"status": "error", "payload": "Maximum retry attempts reached. Service is busy or unavailable."}