import mimetypes
import datetime
import os
from typing import List, Tuple, Dict

from googleapiclient.http import MediaFileUpload

from google_settings.create_service_settings import create_drive_service, create_sheets_service


def upload_files(lst_of_path: List[str], folder_id: str) -> None:
    drive_service = create_drive_service()
    query = f"parents = '{folder_id}'"
    response = drive_service.files().list(q=query).execute()
    files = response.get("files")

    for file in lst_of_path:
        file_name = file.split(os.path.sep)[-1]
        parent_folder_id = folder_id
        starred = True
        file_path = file

        mime_type, _ = mimetypes.guess_type(file_path)
        media_content = MediaFileUpload(file_path, mimetype=mime_type)

        request_body = {"name": file_name, "starred": starred}

        if parent_folder_id:
            request_body["parents"] = [parent_folder_id]

        if not any(file_name == dictionary["name"] for dictionary in files):
            drive_service.files().create(body=request_body, media_body=media_content).execute()


def share_files(excel_link: str, files_folder_mapped: Dict[tuple, str]) -> None:
    service_sheets = create_sheets_service()
    service_drive = create_drive_service()

    SPREADSHEET_ID = excel_link.replace("https://docs.google.com/spreadsheets/d/", "").replace("/edit#gid=0", "")

    response = service_sheets.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="A1:A").execute()
    last_row = len(response["values"])

    response = (
        service_sheets.spreadsheets()
        .values()
        .get(spreadsheetId=SPREADSHEET_ID, majorDimension="ROWS", range=f"A1:B{last_row}")
        .execute()
    )

    for row in response["values"][1:]:
        email = row[0]
        filenames = row[1]
        files_list = filenames.split(",")
        ids = []
        for filename in files_list:
            folder, file = filename.split("/")
            folder_id = (
                service_drive.files()
                .list(q=f"mimeType='application/vnd.google-apps.folder' and name='{folder}'")
                .execute()["files"][0]["id"]
            )
            print(folder_id)
            query = f"name = '{file}' and '{folder_id}' in parents"
            result = service_drive.files().list(q=query).execute()
            ids.append(result["files"][0]["id"])

        request_body = {"role": "reader", "type": "user", "emailAddress": email}

        for id in ids:
            service_drive.permissions().create(
                fileId=id,
                body=request_body,
            ).execute()


def create_user_folder(folder_name: str) -> str:
    drive_service = create_drive_service()
    file_metadata = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
    file = drive_service.files().create(body=file_metadata, fields="id").execute()
    print(f"{folder_name} folder created with id={file.get('id')}")
    return file.get("id")


def get_user_folders(username: str) -> List[str]:
    service_drive = create_drive_service()
    folders = (
        service_drive.files()
        .list(
            q="mimeType = 'application/vnd.google-apps.folder'",
            pageSize=50,
            fields="nextPageToken, files(id, name)",
        )
        .execute()
    )
    return folders


def get_files_from_folder(drive_folder_id: str) -> Tuple[str]:
    service_drive = create_drive_service()
    files = (
        service_drive.files()
        .list(
            q=f"'{drive_folder_id}' in parents",
            pageSize=50,
            fields="nextPageToken, files(id, name, modifiedTime)",
        )
        .execute()
    )
    return files


def get_all_files() -> Tuple[str]:
    service_drive = create_drive_service()
    files = (
        service_drive.files()
        .list(
            pageSize=50,
            fields="nextPageToken, files(id, name, modifiedTime)",
        )
        .execute()
    )
    return files


def delete_files_by_list_id(files_id: List[str]) -> None:
    service_drive = create_drive_service()
    for id in files_id:
        service_drive.files().delete(fileId=id).execute()


def delete_all_files(files):
    service_drive = create_drive_service()
    for dictionary in files["files"]:
        service_drive.files().delete(fileId=dictionary["id"]).execute()


def delete_expired_files(period: int) -> None:
    today = datetime.datetime.today()
    files = get_all_files()

    for file in files["files"]:
        time = file["modifiedTime"]
        modified_time = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        time_delta = today - modified_time

        if time_delta.days >= period:
            delete_files_by_list_id([file["id"]])
