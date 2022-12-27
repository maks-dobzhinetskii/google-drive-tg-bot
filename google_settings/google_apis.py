import os

from googleapiclient.discovery import build
from google.oauth2 import service_account


def create_service(service_account_file, api_name, api_version, *scopes, prefix=''):
    SERVICE_ACCOUNT_FILE = service_account_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
