from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

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


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/api/process-request", response_model=ProcessRequestResponse)
def process_request(payload: ProcessRequestPayload) -> ProcessRequestResponse:
    if not payload.request_id or not payload.user_id:
        raise HTTPException(status_code=400, detail="Invalid request")

    # TODO: Implement queueing / background processing
    return ProcessRequestResponse(status="accepted", request_id=payload.request_id)
