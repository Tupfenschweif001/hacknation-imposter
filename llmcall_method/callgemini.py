import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from supabase import create_client

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
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

def extract_service_type(description: str) -> str:
    """
    Extrahiert den Service-Typ aus der Description
    
    Args:
        description: User's request description
        
    Returns:
        Service type string (e.g., "Arztpraxen", "Zahnarztpraxen")
    """
    description_lower = description.lower()
    
    # Keyword Mapping
    keywords = {
        'zahnarzt': 'Zahnarztpraxen',
        'zahn': 'Zahnarztpraxen',
        'arzt': 'Arztpraxen',
        'hausarzt': 'Hausarztpraxen',
        'allgemeinmedizin': 'Arztpraxen',
        'friseur': 'Friseursalons',
        'frisör': 'Friseursalons',
        'haare': 'Friseursalons',
        'klempner': 'Klempner',
        'sanitär': 'Klempner',
        'elektriker': 'Elektriker',
        'elektro': 'Elektriker',
        'mechaniker': 'Autowerkstätten',
        'werkstatt': 'Autowerkstätten',
        'auto': 'Autowerkstätten',
        'restaurant': 'Restaurants',
        'essen': 'Restaurants',
        'physiotherapie': 'Physiotherapiepraxen',
        'physio': 'Physiotherapiepraxen',
        'massage': 'Massagepraxen',
        'apotheke': 'Apotheken',
    }
    
    # Suche nach Keywords
    for keyword, service in keywords.items():
        if keyword in description_lower:
            return service
    
    # Fallback
    return 'Dienstleister'

def getcontactinfo(street: str, postal_code: str, description: str, radius_km: int = 10) -> list:
    """
    Findet Kontakte in der Nähe basierend auf Description
    
    Args:
        street: Straßenname
        postal_code: Postleitzahl
        description: Beschreibung des gewünschten Services
        radius_km: Suchradius in Kilometern (5, 10, 20)
        
    Returns:
        Liste von Kontakten mit Name und Telefonnummer
    """
    
    load_dotenv()
    
    # Gemini konfigurieren
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set in environment variables.")
    
    genai.configure(api_key=api_key)
    
    # Service-Typ extrahieren
    service_type = extract_service_type(description)
    
    print("\n" + "="*70)
    print("🔍 CONTACT SEARCH")
    print("="*70)
    print(f"📍 Location: {street}, {postal_code}")
    print(f"🎯 Service Type: {service_type}")
    print(f"📏 Radius: {radius_km} km")
    print(f"📝 Description: {description}")
    print("="*70)
    
    # Prompt erstellen
    prompt = f"""Gebe in einem JSON Format ohne sonstigen Inhalt die 10 {service_type} zurück, 
die von der Entfernung am kürzesten von {street} in {postal_code} entfernt sind 
(maximal {radius_km} km Radius).

Für jeden Eintrag gebe zurück:
- name: Name der Praxis/des Geschäfts
- telefonnummer: Telefonnummer im Format 0XXX XXXXXX

Beispiel Format:
[
  {{"name": "Praxis Dr. Müller", "telefonnummer": "0721 123456"}},
  {{"name": "Praxis Dr. Schmidt", "telefonnummer": "0721 234567"}}
]

Gebe NUR das JSON Array zurück, keine zusätzlichen Erklärungen."""
    
    print("\n📤 PROMPT:")
    print("-"*70)
    print(prompt)
    print("-"*70)
    
    # LLM Call
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    llm_result = response.text
    
    print("\n📥 GEMINI RAW OUTPUT:")
    print("-"*70)
    print(llm_result)
    print("-"*70)
    
    # Parse JSON
    extracted_data = []
    
    try:
        # Isolate JSON part
        start_index = llm_result.find('[')
        end_index = llm_result.rfind(']') + 1
        
        if start_index != -1 and end_index != 0:
            json_string = llm_result[start_index:end_index]
            
            # Parse JSON
            full_data = json.loads(json_string)
            
            # Extract name and phone
            for entry in full_data:
                contact_info = {
                    "name": entry.get("name"),
                    "telefonnummer": entry.get("telefonnummer")
                }
                extracted_data.append(contact_info)
            
            print("\n✅ PARSED CONTACTS:")
            print("-"*70)
            for i, contact in enumerate(extracted_data, 1):
                print(f"{i}. {contact['name']} - {contact['telefonnummer']}")
            print("="*70 + "\n")
            
        else:
            print("❌ Error: Could not find JSON array in response")
            
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        print("="*70 + "\n")
    
    return extracted_data


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


# Test-Funktion
if __name__ == "__main__":
    try:
        # Test mit Beispiel-Daten
        contacts = getcontactinfo(
            street="Nancystraße",
            postal_code="76187",
            description="Zahnarzt Termin für Zahnreinigung",
            radius_km=10
        )
        
        print(f"\n✅ Found {len(contacts)} contacts")
        
    except Exception as e:
        print(f"❌ Error: {e}")