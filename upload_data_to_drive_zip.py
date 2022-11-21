import mimetypes

from typing import List
from googleapiclient.http import MediaFileUpload

from google_settings.google_apis import create_service


CLIENT_SECRET_FILE = 'google_settings/client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def upload_files(lst_of_path: List[str]) -> None:
    folder_id = '1lVZH7ZUeYa2Seat-UYFz99TLkrVMa0VQ'
    query = f"parents = '{folder_id}'"
    response = service.files().list(q=query).execute()
    files = response.get('files')

    for file in lst_of_path:
        file_name = file.split('\\')[-1]
        parent_folder_id = folder_id
        starred = True
        file_path = file

        mime_type, _ = mimetypes.guess_type(file_path)
        media_content = MediaFileUpload(file_path, mimetype=mime_type)

        request_body = {'name': file_name, 'starred': starred}

        if parent_folder_id:
            request_body['parents'] = [parent_folder_id]

        if not any(file_name == dictionary['name'] for dictionary in files):
            service.files().create(body=request_body, media_body=media_content).execute()


if __name__ == '__main__':
    lst_of_path = [
        'C:\\Maki\\Uvik\\google-drive-tg-bot\\files\\path.txt',
        'C:\\Maki\\Uvik\\google-drive-tg-bot\\files\\maki.txt',
        'C:\\Maki\\Uvik\\google-drive-tg-bot\\files\\kirya.txt'
    ]

    upload_files(lst_of_path)
