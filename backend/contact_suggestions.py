"""
Contact Suggestions API
Findet passende Kontakte basierend auf User-Profil und Description
"""
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from llmcall_method.callgemini import getcontactinfo, get_supabase_client


async def get_contact_suggestions(user_id: str, description: str, radius_km: int = 10) -> dict:
    """
    Findet Kontakt-Vorschläge für einen User
    
    Args:
        user_id: Supabase User ID
        description: Beschreibung des gewünschten Services
        radius_km: Suchradius in km (5, 10, 20)
        
    Returns:
        Dictionary mit contacts Liste und metadata
    """
    
    try:
        # 1. Lade User Profile aus Supabase
        supabase = get_supabase_client()
        
        print("\n" + "="*70)
        print("🔍 DEBUG: PROFILE LOOKUP")
        print("="*70)
        print(f"📋 Looking for user_id: {user_id}")
        print(f"🔗 Supabase URL: {os.getenv('NEXT_PUBLIC_SUPABASE_URL')}")
        print("-"*70)
        
        # Verwende .execute() statt .single() um Exception zu vermeiden
        profile_response = supabase.table('profiles').select('*').eq('user_id', user_id).execute()
        
        print(f"📊 Query executed successfully")
        print(f"📊 Response data: {profile_response.data}")
        print(f"📊 Number of rows: {len(profile_response.data) if profile_response.data else 0}")
        print("="*70 + "\n")
        
        if not profile_response.data or len(profile_response.data) == 0:
            return {
                "success": False,
                "error": "⚠️ Profile not found! Please go to /profile and complete your profile with your address (street, postal code, city).",
                "contacts": []
            }
        
        profile = profile_response.data[0]
        
        # 2. Extrahiere Adress-Daten
        street = profile.get('street', '')
        house_number = profile.get('house_number', '')
        postal_code = profile.get('postal_code', '')
        city = profile.get('city', '')
        
        # Kombiniere Straße + Hausnummer
        full_street = f"{street} {house_number}".strip() if house_number else street
        
        if not full_street or not postal_code:
            return {
                "success": False,
                "error": "⚠️ Incomplete address! Please go to /profile and add:\n• Street\n• Postal Code\n• City\n\nThese are required to find contacts nearby.",
                "contacts": []
            }
        
        print(f"\n🔍 Searching contacts for user {user_id}")
        print(f"📍 Address: {full_street}, {postal_code} {city}")
        print(f"📝 Description: {description}")
        print(f"📏 Radius: {radius_km} km\n")
        
        # 3. Rufe getcontactinfo auf
        contacts = getcontactinfo(
            street=full_street,
            postal_code=postal_code,
            description=description,
            radius_km=radius_km
        )
        
        # 4. Return Ergebnis
        return {
            "success": True,
            "contacts": contacts,
            "metadata": {
                "location": f"{full_street}, {postal_code} {city}",
                "radius_km": radius_km,
                "count": len(contacts)
            }
        }
        
    except Exception as e:
        print(f"❌ Error in get_contact_suggestions: {e}")
        return {
            "success": False,
            "error": str(e),
            "contacts": []
        }


# Test-Funktion
if __name__ == "__main__":
    import asyncio
    
    async def test():
        # Test mit Beispiel User ID (ersetze mit echter ID)
        result = await get_contact_suggestions(
            user_id="test-user-id",
            description="Zahnarzt Termin für Zahnreinigung",
            radius_km=10
        )
        
        print("\n" + "="*70)
        print("TEST RESULT:")
        print("="*70)
        print(f"Success: {result['success']}")
        print(f"Contacts found: {len(result.get('contacts', []))}")
        
        if result['success']:
            for i, contact in enumerate(result['contacts'], 1):
                print(f"{i}. {contact['name']} - {contact['telefonnummer']}")
        else:
            print(f"Error: {result.get('error')}")
        
        print("="*70)
    
    asyncio.run(test())