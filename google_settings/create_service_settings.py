from googleapiclient.discovery import Resource

from google_settings.google_apis import create_service


CLIENT_SECRET_FILE = 'google_settings/client_secrets.json'


def create_sheets_service() -> Resource:
    API_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    return create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def create_drive_service() -> Resource:
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    return create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
