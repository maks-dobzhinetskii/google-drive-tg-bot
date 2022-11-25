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
        email = row[0]
        filenames = row[1]
        files_list = filenames.split(",")
        ids = []
        for filename in files_list:
            query = f"name = '{filename}'"
            result = service_drive.files().list(q=query).execute()
            ids.append(result["files"][0]["id"])

        request_body = {"role": "reader", "type": "user", "emailAddress": email}

        for id in ids:
            service_drive.permissions().create(
                fileId=id,
                body=request_body,
            ).execute()


if __name__ == "__main__":
    excel_link = "https://docs.google.com/spreadsheets/d/153LPQX66xGOzc32wNZrXJkf1xNv3QzTaPcFO_LofSWs/edit#gid=0"
    sharing_file_link(excel_link)
