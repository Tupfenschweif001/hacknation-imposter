from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
from datetime import datetime, timedelta
import pytz
 
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
 
def authenticate_google_calendar():
    """Authenticate and return the Google Calendar service."""
    creds = None
 
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
 
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google-calender-api/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
 
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
 
    service = build('calendar', 'v3', credentials=creds)
    return service
 
def is_user_busy(service, check_time_start, check_time_end, calendar_id='primary'):
    # Convert datetime to RFC3339 format
    time_min = check_time_start.isoformat()
    time_max = check_time_end.isoformat()
 
    # Use freebusy query to check availability
    body = {
        "timeMin": time_min,
        "timeMax": time_max,
        "items": [{"id": calendar_id}]
    }
 
    freebusy_result = service.freebusy().query(body=body).execute()
    busy_periods = freebusy_result['calendars'][calendar_id]['busy']
 
    is_busy = len(busy_periods) > 0
 
    return is_busy, busy_periods
 
def get_events_at_time(service, check_time_start, check_time_end, calendar_id='primary'):
    time_min = check_time_start.isoformat()
    time_max = check_time_end.isoformat()
 
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
 
    events = events_result.get('items', [])
 
    return events
 
def main():
    # Authenticate
    service = authenticate_google_calendar()
 
    # Define the time to check (example: today at 2 PM for 1 hour)
    timezone = pytz.timezone('America/New_York')  # Change to your timezone
 
    # Check if busy today at 2 PM
    check_start = datetime.now(timezone).replace(hour=14, minute=0, second=0, microsecond=0)
    check_end = check_start + timedelta(hours=1)
 
    print(f"Checking availability from {check_start} to {check_end}")
 
    # Method 1: Using freebusy API (faster, but less details)
    is_busy, busy_periods = is_user_busy(service, check_start, check_end)
 
    if is_busy:
        print("❌ User is BUSY during this time")
        print(f"Busy periods: {busy_periods}")
    else:
        print("✅ User is FREE during this time")
 
    print("\n" + "="*50 + "\n")
 
    # Method 2: Using events API (more details about events)
    events = get_events_at_time(service, check_start, check_end)
 
    if events:
        print(f"Found {len(events)} event(s) during this time:")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            summary = event.get('summary', 'No title')
            print(f"  - {summary}")
            print(f"    From: {start}")
            print(f"    To: {end}")
    else:
        print("No events found during this time")
 
if __name__ == '__main__':
    main()
