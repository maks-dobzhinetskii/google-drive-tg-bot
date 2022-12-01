import os
import zipfile
from datetime import datetime, timedelta
from dataclasses import dataclass

import telebot

from google_utils import upload_data_to_drive_excel, upload_data_to_drive_zip
from google_utils.utils import create_user_folder
from tg_bot.bot import bot
from tg_bot.markup import home_markup
from tg_bot.states import UploadStates
from users.orm import (
    create_folder,
    create_message,
    create_user,
    get_folder_info_by_id_drive_folder,
    get_query_by_media_group_id,
    session,
)


media_groups = dict()


@dataclass
class MediaGroup:
    items: dict
    handler_start_time: datetime
    message_posted: bool
    result_message: telebot.types.Message
    drive_folder_id: str


EXP_TIME = timedelta(minutes=3)


@bot.message_handler(state=UploadStates.direct_upload, content_types=["document"])
async def handle_direct_upload(message: telebot.types.Message):
    user = create_user(message.from_user.username)
    group_id = message.media_group_id
    if group_id not in media_groups:
        media_groups[group_id] = MediaGroup({}, datetime.now(), False, None, None)
    media_groups[group_id].items.update({message.document.file_id: False})
    doc_messages = session.scalar(get_query_by_media_group_id(group_id))
    if not doc_messages and not media_groups[group_id].message_posted:
        media_groups[group_id].message_posted = True
        result_message = await bot.send_message(
            message.chat.id, "Downloading your files", disable_web_page_preview=True
        )
        media_groups[group_id].result_message = result_message
    file_path = await bot.get_file(message.document.file_id)

    downloaded_file = await bot.download_file(file_path.file_path)

    relative_download_folder_path = (
        f"downloads/direct_upload/{message.from_user.username}/{datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}"
    )
    if not os.path.exists(relative_download_folder_path):
        os.makedirs(relative_download_folder_path, exist_ok=True)
    file_name = os.path.join(relative_download_folder_path, message.document.file_name)
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)

    folder_id = None
    if media_groups[group_id].drive_folder_id:
        folder_id = get_folder_info_by_id_drive_folder(media_groups[group_id].drive_folder_id).id
    else:
        folder_name = f"{message.from_user.username}_{datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}"
        drive_folder_id = create_user_folder(folder_name)
        media_groups[group_id].drive_folder_id = drive_folder_id
        folder = create_folder(folder_name, drive_folder_id)
        folder_id = folder.id

    create_message(group_id, message.document.file_name, folder_id, user.id)

    upload_data_to_drive_zip.upload_files([os.path.abspath(file_name)], media_groups[group_id].drive_folder_id)

    if datetime.now() - media_groups[group_id].handler_start_time > EXP_TIME:
        media_groups.pop(group_id)
    media_groups[group_id].items[message.document.file_id] = True
    if all(media_groups[group_id].items.values()):
        await bot.edit_message_text(
            chat_id=media_groups[group_id].result_message.chat.id,
            message_id=media_groups[group_id].result_message.id,
            text="Done!",
        )
        await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
        await bot.send_message(message.chat.id, "Choose next action", reply_markup=home_markup())


@bot.message_handler(state=UploadStates.zip_upload, content_types=["document"])
async def handle_zip_upload(message: telebot.types.Message):
    # TODO check if document mime_type is application/zip
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
