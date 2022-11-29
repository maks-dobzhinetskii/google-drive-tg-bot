import os
import zipfile

import telebot

from google_utils import upload_data_to_drive_excel
from google_utils import upload_data_to_drive_zip

from datetime import datetime
from tg_bot.bot import bot
from tg_bot.markup import home_markup
from tg_bot.states import UploadStates
from google_utils.utils import create_user_folder


@bot.message_handler(state=UploadStates.direct_upload, content_types=["document"])
async def handle_direct_upload(message: telebot.types.Message):
    # TODO: start: check if messages media group id is already in db
    result_message = await bot.send_message(message.chat.id, "Downloading your file...", disable_web_page_preview=True)
    file_path = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_path.file_path)
    # TODO: get folder id from db if there already were messages with currnet media group id
    drive_folder_name = f"{message.from_user.username}_{datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}"
    folder_id = create_user_folder(drive_folder_name)
    relative_download_folder_path = (
        f"downloads/direct_upload/{message.from_user.username}/{datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}"
    )
    if not os.path.exists(relative_download_folder_path):
        os.makedirs(relative_download_folder_path, exist_ok=True)
    file_name = os.path.join(relative_download_folder_path, message.document.file_name)
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)

    upload_data_to_drive_zip.upload_files([os.path.abspath(file_name)], folder_id)

    # TODO: end: check if messages media group id is already in db
    await bot.edit_message_text(chat_id=message.chat.id, message_id=result_message.id, text="Done!")
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.send_message(message.chat.id, "Choose next action", reply_markup=home_markup())


@bot.message_handler(state=UploadStates.zip_upload, content_types=["document"])
async def handle_zip_upload(message: telebot.types.Message):
    result_message = await bot.send_message(message.chat.id, "Downloading...", disable_web_page_preview=True)
    file_path = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_path.file_path)
    drive_folder_name = f"{message.from_user.username}_{datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}"
    folder_id = create_user_folder(drive_folder_name)
    relative_download_folder_path = (
        f"downloads/zip_upload/{message.from_user.username}/{datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}"
    )
    file_name = os.path.join(relative_download_folder_path, message.document.file_name)
    unzipped_folder_name = file_name.replace(".zip", "")
    if not os.path.exists(unzipped_folder_name):
        os.makedirs(unzipped_folder_name, exist_ok=True)
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)

    with zipfile.ZipFile(file_name, "r") as zipf:
        zipf.extractall(unzipped_folder_name)
    paths = os.listdir(unzipped_folder_name)
    if unzipped_folder_name[-1] == os.path.sep:
        paths = [f"{unzipped_folder_name}{path}" for path in os.listdir(unzipped_folder_name)]
    else:
        paths = [f"{unzipped_folder_name}/{path}" for path in os.listdir(unzipped_folder_name)]

    upload_data_to_drive_zip.upload_files(paths, folder_id)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=result_message.id, text="Done!")
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.send_message(message.chat.id, "Choose next action", reply_markup=home_markup())


@bot.message_handler(state=UploadStates.excel_upload, content_types=["document"])
async def handle_excel_upload(message: telebot.types.Message):
    result_message = await bot.send_message(message.chat.id, "Downloading...", disable_web_page_preview=True)
    file_path = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_path.file_path)
    drive_folder_name = f"{message.from_user.username}_{datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}"
    folder_id = create_user_folder(drive_folder_name)
    relative_download_folder_path = (
        f"downloads/excel_upload/{message.from_user.username}/{datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}"
    )
    if not os.path.exists(relative_download_folder_path):
        os.makedirs(relative_download_folder_path, exist_ok=True)
    file_name = os.path.join(relative_download_folder_path, message.document.file_name)
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)

    upload_data_to_drive_excel.upload_files(os.path.abspath(file_name), folder_id)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=result_message.id, text="Done!")
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.send_message(message.chat.id, "Choose next action", reply_markup=home_markup())
