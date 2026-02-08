from __future__ import annotations

import asyncio
import time
from datetime import datetime, timedelta, time as dtime
import os
import sys
from pathlib import Path
from typing import Optional

# Füge das Root-Verzeichnis zum Python-Pfad hinzu, damit 'twillio' gefunden wird
sys.path.append(str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from twillio.start_call import start_call
from backend.contact_suggestions import get_contact_suggestions

load_dotenv()

app = FastAPI(title="Hacknation Backend", version="0.1.0")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserProfile(BaseModel):
    username: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class ProcessRequestPayload(BaseModel):
    request_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    callback_number: str = Field(..., min_length=0)
    number_to_call: Optional[str] = None
    preferred_time: str = Field(..., min_length=1)
    user_profile: Optional[UserProfile] = None


class ProcessRequestResponse(BaseModel):
    status: str
    request_id: str


class ContactSuggestionsPayload(BaseModel):
    user_id: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    radius_km: int = Field(default=10, ge=5, le=20)


class ContactSuggestionsResponse(BaseModel):
    success: bool
    contacts: list
    metadata: Optional[dict] = None
    error: Optional[str] = None


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/api/get-contact-suggestions", response_model=ContactSuggestionsResponse)
async def get_contact_suggestions_endpoint(payload: ContactSuggestionsPayload) -> ContactSuggestionsResponse:
    """
    Findet Kontakt-Vorschläge basierend auf User-Profil und Description
    """
    try:
        result = await get_contact_suggestions(
            user_id=payload.user_id,
            description=payload.description,
            radius_km=payload.radius_km
        )
        
        return ContactSuggestionsResponse(**result)
        
    except Exception as e:
        print(f"❌ Error in contact suggestions endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/process-request", response_model=ProcessRequestResponse)
async def process_request(payload: ProcessRequestPayload, background_tasks: BackgroundTasks) -> ProcessRequestResponse:
    if not payload.request_id or not payload.user_id:
        raise HTTPException(status_code=400, detail="Invalid request")

    # Der Task wird in den Hintergrund verschoben. Die API antwortet SOFORT.
    background_tasks.add_task(
        start_new_call, 
        request_id=payload.request_id,
        number=payload.number_to_call,
        title=payload.title,
        description=payload.description
    )
    
    return ProcessRequestResponse(status="accepted", request_id=payload.request_id)


async def start_new_call(request_id, number=None, title=None, description=None):
    """
    Startet den Anruf asynchron. Wenn wir außerhalb der Geschäftszeiten sind,
    wartet diese Funktion (non-blocking) bis zur nächsten Startzeit.
    """
    if is_business_hours():
        start_call(number=number, request_id=request_id, title=title, description=description)
        return

    run_at = next_business_datetime()
    delay_seconds = max(0, (run_at - datetime.now()).total_seconds())
    
    if delay_seconds > 0:
        print(f"Außerhalb der Geschäftszeiten. Warte {delay_seconds:.0f} Sekunden ...")
        # asyncio.sleep blockiert den Server NICHT. time.sleep würde alles anhalten.
        await asyncio.sleep(delay_seconds)

    print("Geschäftszeit erreicht. Starte Anruf jetzt.")
    start_call(number=number, request_id=request_id, title=title, description=description)
        


def is_business_hours():
    """
    Prüft ob aktuell Geschäftszeiten sind.
    Montag-Freitag, 08:00-18:00 Uhr
    """
    return True
    now = datetime.now()
    
    # Wochenende
    if now.weekday() >= 5:  # 5=Samstag, 6=Sonntag
        return False
    
    # Außerhalb 08:00-18:00
    if now.hour < 8 or now.hour >= 18:
        return False
    
    return True


def next_business_datetime(now: datetime | None = None) -> datetime:
    current = now or datetime.now()

    # If it's weekend, jump to next Monday 08:00
    if current.weekday() >= 5:
        days_until_monday = 7 - current.weekday()
        next_day = (current + timedelta(days=days_until_monday)).date()
        return datetime.combine(next_day, dtime(hour=8, minute=0))

    # If before business hours, schedule for today 08:00
    if current.hour < 8:
        return datetime.combine(current.date(), dtime(hour=8, minute=0))

    # If after business hours, schedule for next weekday 08:00
    if current.hour >= 18:
        next_day = current.date() + timedelta(days=1)
        while next_day.weekday() >= 5:
            next_day += timedelta(days=1)
        return datetime.combine(next_day, dtime(hour=8, minute=0))

    return current



