from google_settings.create_service_settings import create_drive_service, create_sheets_service


def sharing_file_link(excel_link: str) -> None:
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
        print(row)
        email = row[0]
        file_id = row[1:]

        print(email)
        request_body = {"role": "reader", "type": "user", "emailAddress": email}

        for file in file_id[0].split(","):
            service_drive.permissions().create(
                fileId=file,
                body=request_body,
            ).execute()


if __name__ == "__main__":
    excel_link = "https://docs.google.com/spreadsheets/d/153LPQX66xGOzc32wNZrXJkf1xNv3QzTaPcFO_LofSWs/edit#gid=0"
    sharing_file_link(excel_link)
