from google_settings.create_service_settings import create_drive_service, create_sheets_service


def sharing_file_link(excel_link: str) -> None:
    service_sheets = create_sheets_service()
    service_drive = create_drive_service()

    spreadsheet_id = excel_link.split('/')

    response = service_sheets.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id[-2],
        majorDimension='ROWS',
        range='Info!A1:B3'
    ).execute()

    for row in response['values'][1:]:
        email = row[0]
        file_id = row[1:]

        request_body = {"role": "reader", "type": "user", "emailAddress": email}

        for file in file_id[0].split(','):
            service_drive.permissions().create(
                fileId=file,
                body=request_body,
            ).execute()


if __name__ == '__main__':
    excel_link = 'https://docs.google.com/spreadsheets/d/153LPQX66xGOzc32wNZrXJkf1xNv3QzTaPcFO_LofSWs/edit#gid=0'
    sharing_file_link(excel_link)
