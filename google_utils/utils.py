from google_settings.create_service_settings import create_drive_service


def create_user_folder(folder_name: str) -> str:
    drive_service = create_drive_service()
    file_metadata = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
    file = drive_service.files().create(body=file_metadata, fields="id").execute()
    print(f"{folder_name} folder created with id={file.get('id')}")
    return file.get("id")
