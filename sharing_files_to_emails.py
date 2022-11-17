import pandas as pd

from google_settings.google_apis import create_service


CLIENT_SECRET_FILE = "google_settings/client_secrets.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

file_list = pd.read_excel("template_sharing.xlsx", sheet_name="files")
file_list = file_list.fillna("")


def sharing_file_link():
    for row in file_list.iterrows():
        email = row[1]["Email"]
        file_id = row[1]["File Id"]

        request_body = {"role": "reader", "type": "user", "emailAddress": email}

        service.permissions().create(
            fileId=file_id,
            body=request_body,
        ).execute()


if __name__ == "__main__":
    sharing_file_link()
