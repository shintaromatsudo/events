import datetime
import os.path

from dateutil import tz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


class Schedule:
    def auth(self) -> Credentials:
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        self.creds = creds

    def execute(self, text: str):
        local_tz = tz.tzlocal()
        now = datetime.datetime.now(local_tz)
        today_midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=2)
        tomorrow_midnight = today_midnight + datetime.timedelta(days=1)

        if "next" in text:
            return self.get_next_event(now.isoformat())
        elif "today" in text:
            return self.get_events(now.isoformat(), today_midnight.isoformat())
        elif "tomorrow" in text:
            return self.get_events(today_midnight.isoformat(), tomorrow_midnight.isoformat())


    def get_next_event(self, now: str):
        try:
            service = build("calendar", "v3", credentials=self.creds)
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    eventTypes="default",
                    timeMin=now,
                    singleEvents=True,
                    orderBy="startTime",
                    maxResults=1,
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                return "No upcoming events found."

            event = events[0]
            start = event["start"]["dateTime"].split("T")
            date = start[0]
            time = start[1].split("+")[0]
            # print(date, time, event["summary"])

            return f"{date} {time} {event['summary']}"

        except HttpError as error:
            print(f"An error occurred: {error}")
            return "An error occurred"

    def get_events(self, start: datetime, end: datetime):
        try:
            service = build("calendar", "v3", credentials=self.creds)
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    eventTypes="default",
                    timeMin=start,
                    timeMax=end,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                return "No upcoming events found."

            events_str = ""

            for event in events:
                start = event["start"]["dateTime"].split("T")[1].split("+")[0]
                events_str += f"{start} {event['summary']}\n"

            # print(events_str)
            return events_str

        except HttpError as error:
            print(f"An error occurred: {error}")
            return "An error occurred"

if __name__ == "__main__":
    s = Schedule()
    s.auth()
    print(s.execute("tomorrow"))
