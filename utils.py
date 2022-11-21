from googleapiclient.http import MediaFileUpload
from typing import List, Any


def overwrite_files(files: List[dict], file_name: str, service: Any, request_body: dict, media_content: MediaFileUpload) -> None:
    for dictionary in files:
        if file_name == dictionary['name']:
            result = input(f'Do you want to overwrite {file_name} file?')
            if int(result):
                service.files().delete(fileId=dictionary['id']).execute()
                service.files().create(body=request_body, media_body=media_content).execute()