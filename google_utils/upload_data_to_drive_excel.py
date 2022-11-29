import mimetypes
import pandas as pd

from googleapiclient.http import MediaFileUpload

from google_settings.create_service_settings import create_drive_service

from users.database import engine
from users.models import metadata


metadata.create_all(engine)


def upload_files(excel_file_path: str, folder_id: str) -> None:
    drive_service = create_drive_service()
    file_list = pd.read_excel(excel_file_path, sheet_name="files")
    file_list = file_list.fillna("")

    query = f"parents = '{folder_id}'"
    response = drive_service.files().list(q=query).execute()
    files = response.get("files")

    for row in file_list.iterrows():
        file_name = row[1]["File Name"]
        parent_folder_id = row[1]["Folder Id"]
        starred = row[1]["Starred"]
        file_path = row[1]["File Path"]

        mime_type, _ = mimetypes.guess_type(file_path)
        media_content = MediaFileUpload(file_path, mimetype=mime_type)

        request_body = {"name": file_name, "starred": starred}

        if parent_folder_id:
            request_body["parents"] = [parent_folder_id]

        if not any(file_name == dictionary["name"] for dictionary in files):
            drive_service.files().create(body=request_body, media_body=media_content).execute()


if __name__ == "__main__":
    excel_file_path = "template_upload.xlsx"
    upload_files(excel_file_path, "1lVZH7ZUeYa2Seat-UYFz99TLkrVMa0VQ")
