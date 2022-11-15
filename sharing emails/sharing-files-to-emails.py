import pandas as pd

from google_apis import create_service

from sending_emails import send_email


CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

file_list = pd.read_excel('template.xlsx', sheet_name='files')
file_list = file_list.fillna('')


def sharing_file_link():
    for row in file_list.iterrows():
        email = row[1]['Email']
        file_id = row[1]['File Id']


        request_body = {
            'role': 'reader',
            'type': 'anyone'
        }

        response_permission = service.permissions().create(
            fileId=file_id,
            body=request_body
        ).execute()

        print(response_permission)

        response_share_link = service.files().get(
            fileId=file_id,
            fields='webViewLink'
        ).execute()

        send_email(email, response_share_link['webViewLink'])

        service.permissions().delete(
            fileId=file_id,
            permissionId='anyoneWithLink'
        ).execute()


if __name__ == '__main__':
    sharing_file_link()