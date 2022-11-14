import mimetypes
import pandas as pd

from googleapiclient.http import MediaFileUpload
from google_apis import create_service

client_file = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
service = create_service(client_file, API_NAME, API_VERSION, SCOPES)

file_list = pd.read_excel('template.xlsx', sheet_name='files')
file_list = file_list.fillna('')


def upload_files() -> None:
    for row in file_list.iterrows():
        file_name = row[1]['File Name']
        parent_folder_id = row[1]['Fold er Id']
        starred = row[1]['Starred']
        file_path = row[1]['File Path']

        mime_type, _ = mimetypes.guess_type(file_path)
        media_content = MediaFileUpload(file_path)

        request_body = {
            'name': file_name,
            'starred': starred
        }

        if parent_folder_id:
            request_body['parents'] = [parent_folder_id]

        service.files().create(
            body=request_body,
            media_body=media_content
        ).execute()


if __name__ == '__main__':
    upload_files()
