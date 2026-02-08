import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

# from elevenlabs import ElevenLabs
 
straße = "Nancystraße"
postleitzahl = "76187"

load_dotenv()
# Gemini konfigurieren
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
 
# 1. LLM-Request mit Gemini (kostenlos!)
model = genai.GenerativeModel('gemini-2.5-flash')  # Kostenlose Version
response = model.generate_content("Gebe in einem json Format ohne sonstigen Inhalt die 10 Arztpraxen die von der Entfernung am kürzesten von {straße} in {postleitzahl} entfernt sind mit den zugehörigen Telephonnummern")
llm_result = response.text

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)
 
print(f"Gemini sagt: {llm_result}")

output_filename = "contacts.json"
extracted_data = []

try:
    # 1. Isolate the JSON part of the string
    start_index = llm_result.find('[')
    end_index = llm_result.rfind(']') + 1

    if start_index != -1 and end_index != 0:
        json_string = llm_result[start_index:end_index]

        # 2. Parse the string into a Python list of dictionaries
        full_data = json.loads(json_string)

        # 3. Process the data to extract only the name and phone number
        for entry in full_data:
            contact_info = {
                "name": entry.get("name"),
                "telefonnummer": entry.get("telefonnummer")
            }
            extracted_data.append(contact_info)

        # 4. Save the newly created list to a JSON file
        with open(output_filename, 'w', encoding='utf-8') as f:
            # Use ensure_ascii=False to correctly save characters like 'ü'
            json.dump(extracted_data, f, indent=4, ensure_ascii=False)
        print(f"Successfully processed the data and saved it to '{output_filename}'")

    else:
        print("Error: Could not find a JSON list ('[...]') in the provided text.")
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}") ####
