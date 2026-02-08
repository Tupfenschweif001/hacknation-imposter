import os
from dotenv import load_dotenv
import google.generativeai as genai
from supabase import create_client

# from elevenlabs import ElevenLabs
 
load_dotenv()

def get_supabase_client():
    url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
    key = os.environ.get("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    if not url or not key:
         # Fallback to standard env vars if NEXT_PUBLIC aliases are not used
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("Supabase URL or Key not set in environment variables.")
    return create_client(url, key)

def generate_response(prompt):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set in environment variables.")

    # Gemini konfigurieren
    genai.configure(api_key=api_key)
    
    # 1. LLM-Request mit Gemini (kostenlos!)
    # Available models: gemini-2.0-flash, gemini-2.5-flash, etc.
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    try:
        llm_result = generate_response("Erkläre mir Quantenphysik kurz")
        print(f"Gemini sagt: {llm_result}")
    except Exception as e:
        print(f"Error: {e}")

def generate_llm_reply(user_input, history):
    prompt = f"""
    You are a personal AI assistant calling a service provider (e.g., doctor's office, craftsman).
    Goal: Schedule an appointment for your client.
    
    The receptionist/person on the other end just said: "{user_input}"
    
    Your task:
    - If they offer a time/date, accept it politely ("That works perfectly, thank you.").
    - If they ask for patient/client details, provide them briefly or invent a name (e.g., "Max Mustermann") if not specified.
    - If they ask what the issue is, refer to the request context implicitly or repeat the core issue briefly.
    - Keep it short, polite, and natural (max 2 sentences).

    History: {history}
    """
    return generate_response(prompt)


def generate_llm_start(request_id, title=None, description=None):
    request_data = {}
    
    # 1. Daten aus Parametern nutzen (falls vorhanden)
    if title and description:
        request_data = {'title': title, 'description': description}
    # 2. Sonst DB-Lookup (falls ID vorhanden)
    elif request_id:
        try:
            supabase = get_supabase_client()
            response = supabase.table('requests').select('*').eq('id', request_id).execute()
            
            if response.data:
                request_data = response.data[0]
        except Exception as e:
            print(f"Error fetching request: {e}")
            
    # Fallback Data
    if not request_data:
        request_data = {
            'title': 'a general check-up', 
            'description': 'Routine appointment.'
        }

    prompt = f"""
    You are a personal AI assistant calling a service provider (like a doctor or mechanic) on behalf of your client.
    
    Reason for call:
    - Topic: {request_data.get('title', 'N/A')}
    - Details: {request_data.get('description', 'N/A')}
    
    Task:
    Generate a natural, polite opening for the phone call.
    1. State that you are an AI assistant calling on behalf of a client to schedule an appointment for "{request_data.get('title')}".
    2. Ask politely for the next available time slot.
    
    Keep it mostly short (2 sentences max). Do NOT use bracket placeholders like [Your Name]. Just say "my client".
    """
    
    return generate_response(prompt)