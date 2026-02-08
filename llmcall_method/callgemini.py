import os
import google.generativeai as genai

# from elevenlabs import ElevenLabs
 
# Gemini konfigurieren
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
 
# 1. LLM-Request mit Gemini (kostenlos!)
model = genai.GenerativeModel('gemini-2.5-flash')  # Kostenlose Version
response = model.generate_content("Erkläre mir Quantenphysik kurz")
llm_result = response.text

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)
 
print(f"Gemini sagt: {llm_result}")