import os

from googleapiclient.discovery import build
from google.oauth2 import service_account


def create_service(service_account_file, api_name, api_version, *scopes, prefix=''):
    SERVICE_ACCOUNT_FILE = service_account_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    working_dir = os.getcwd()
    token_dir = 'token_files'
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.pickle'

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        os.remove(os.path.join(working_dir, token_dir, pickle_file))
        return None
