from googleapiclient.discovery import Resource

from google_settings.google_apis import create_service


SERVICE_ACCOUNT_FILE = 'google_settings/bold-gearbox-368613-432f3488f994.json'


def create_sheets_service() -> Resource:
    API_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    return create_service(SERVICE_ACCOUNT_FILE, API_NAME, API_VERSION, SCOPES)


def create_drive_service() -> Resource:
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    return create_service(SERVICE_ACCOUNT_FILE, API_NAME, API_VERSION, SCOPES)
