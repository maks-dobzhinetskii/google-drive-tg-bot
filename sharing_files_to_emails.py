from google_settings.google_apis import create_service
from sheet2api import Sheet2APIClient


CLIENT_SECRET_FILE = "google_settings/client_secrets.json"
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]
service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def sharing_file_link(excel_link: str) -> None:
    client = Sheet2APIClient(api_url=excel_link)

    for row in client.get_rows():
        email = row["Email"]
        file_id = row["File Id"]

        request_body = {"role": "reader", "type": "user", "emailAddress": email}

        for file in file_id.split(","):
            service.permissions().create(
                fileId=file,
                body=request_body,
            ).execute()


if __name__ == "__main__":
    excel_link = "https://sheet2api.com/v1/cmLywK32QWC5/%D0%9D%D0%BE%D0%B2%D0%B0%D1%8F%20%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B0"
    sharing_file_link(excel_link)
