"""
Appointment Booking Agent mit Gemini LLM
Verwaltet die Konversation für Terminbuchungen
"""
import os
from typing import Dict, Optional, List
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class AppointmentAgent:
    """
    KI-Agent für Terminbuchungen via Telefon
    Nutzt Gemini LLM für natürliche Konversation
    """
    
    def __init__(self):
        """Initialisiere den Agent mit Gemini"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY nicht in .env gefunden!")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.conversation_history: List[str] = []
        self.request_context: Dict = {}
        self.system_prompt: str = ""
    
    def set_context(self, request_data: Dict):
        """
        Setze den Kontext für den Agenten basierend auf Request-Daten
        
        Args:
            request_data: Dictionary mit Request-Informationen
                - title: Titel des Requests
                - description: Beschreibung
                - preferred_time: Bevorzugte Zeit
                - user_profile: User-Profil Daten
        """
        self.request_context = request_data
        
        # Extrahiere relevante Informationen
        title = request_data.get('title', 'Termin')
        description = request_data.get('description', '')
        preferred_time = request_data.get('preferred_time', 'so bald wie möglich')
        
        user_profile = request_data.get('user_profile', {})
        user_city = user_profile.get('city', '')
        user_name = user_profile.get('username', '')
        
        # Erstelle System Prompt mit Kontext
        self.system_prompt = f"""Du bist ein freundlicher, professioneller Telefon-Assistent, der Termine bucht.

DEINE AUFGABE:
{title}

DETAILS:
{description}

BEVORZUGTE ZEIT:
{preferred_time}

KUNDE:
Name: {user_name}
Stadt: {user_city}

DEIN ZIEL:
1. Begrüße den Angerufenen höflich und professionell
2. Erkläre kurz den Grund des Anrufs
3. Frage nach verfügbaren Terminen im gewünschten Zeitraum
4. Notiere den Termin und bestätige ihn
5. Bedanke dich und beende das Gespräch höflich

WICHTIGE REGELN:
- Sei SEHR kurz und präzise (maximal 2-3 kurze Sätze pro Antwort)
- Sprich natürlich und freundlich, aber professionell
- Stelle nur EINE Frage pro Antwort
- Wenn kein Termin verfügbar ist: Frage nach Rückruf-Möglichkeit
- Wenn der Gesprächspartner nicht zuständig ist: Frage nach der richtigen Person
- Beende das Gespräch, sobald ein Termin bestätigt wurde

BEISPIEL KONVERSATION:
Agent: "Guten Tag! Hier spricht der Termin-Service. Ich rufe an, um einen Arzttermin für Herrn Müller zu vereinbaren. Haben Sie gerade einen Moment Zeit?"
User: "Ja, gerne."
Agent: "Wunderbar! Wir suchen einen Termin für nächste Woche. Welche Tage hätten Sie verfügbar?"
User: "Mittwoch um 14 Uhr wäre möglich."
Agent: "Perfekt! Mittwoch, 14 Uhr ist notiert. Vielen Dank und einen schönen Tag!"
"""
    
    def get_response(self, user_input: Optional[str] = None) -> str:
        """
        Generiere eine Antwort basierend auf User Input
        
        Args:
            user_input: Was der User gesagt hat (None für erste Nachricht)
            
        Returns:
            Die generierte Antwort des Agenten
        """
        
        if not user_input:
            # Erste Nachricht - Begrüßung
            prompt = f"""{self.system_prompt}

Generiere jetzt die ERSTE Begrüßung für den Anruf.
Sei kurz, freundlich und erkläre den Grund des Anrufs.
Maximal 2-3 kurze Sätze!"""
        else:
            # Füge User Input zur History hinzu
            self.conversation_history.append(f"User: {user_input}")
            
            # Generiere Antwort basierend auf Konversation
            history_text = "\n".join(self.conversation_history[-6:])  # Nur letzte 6 Nachrichten
            
            prompt = f"""{self.system_prompt}

BISHERIGE KONVERSATION:
{history_text}

User sagt jetzt: "{user_input}"

Generiere eine passende, KURZE Antwort (maximal 2-3 kurze Sätze).
Stelle nur EINE Frage.
Wenn ein Termin bestätigt wurde, beende das Gespräch höflich."""
        
        try:
            # Generiere Antwort mit Gemini
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=150,  # Kurze Antworten erzwingen
                )
            )
            
            agent_response = response.text.strip()
            
            # Füge zur History hinzu
            self.conversation_history.append(f"Agent: {agent_response}")
            
            return agent_response
            
        except Exception as e:
            print(f"❌ Fehler bei LLM Call: {e}")
            # Fallback
            if not user_input:
                return "Guten Tag! Hier spricht der Termin-Service. Ich möchte einen Termin vereinbaren. Haben Sie einen Moment Zeit?"
            else:
                return "Entschuldigung, könnten Sie das bitte wiederholen?"
    
    def get_conversation_summary(self) -> str:
        """
        Erstelle eine Zusammenfassung der Konversation
        
        Returns:
            Zusammenfassung als String
        """
        if not self.conversation_history:
            return "Keine Konversation vorhanden."
        
        history_text = "\n".join(self.conversation_history)
        
        prompt = f"""Fasse diese Telefon-Konversation kurz zusammen:

{history_text}

Erstelle eine kurze Zusammenfassung mit:
- Wurde ein Termin vereinbart? (Ja/Nein)
- Wenn ja: Wann?
- Besondere Notizen

Maximal 3-4 Sätze."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Fehler bei Summary: {e}")
            return "Zusammenfassung konnte nicht erstellt werden."
    
    def reset(self):
        """Setze den Agent zurück für einen neuen Call"""
        self.conversation_history = []
        self.request_context = {}
        self.system_prompt = ""


# Test-Funktion
if __name__ == "__main__":
    # Test mit Beispiel-Daten
    agent = AppointmentAgent()
    
    test_request = {
        'title': 'Arzttermin vereinbaren',
        'description': 'Allgemeine Untersuchung beim Hausarzt',
        'preferred_time': 'nächste Woche, vormittags',
        'user_profile': {
            'username': 'Max Mustermann',
            'city': 'Berlin'
        }
    }
    
    agent.set_context(test_request)
    
    # Erste Nachricht
    print("Agent:", agent.get_response())
    
    # Simuliere Konversation
    print("\nUser: Ja, gerne.")
    print("Agent:", agent.get_response("Ja, gerne."))
    
    print("\nUser: Mittwoch um 10 Uhr wäre gut.")
    print("Agent:", agent.get_response("Mittwoch um 10 Uhr wäre gut."))
    
    # Summary
    print("\n--- SUMMARY ---")
    print(agent.get_conversation_summary())