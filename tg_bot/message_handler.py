import os

import telebot

import upload_data_to_drive_zip

from datetime import datetime
from sharing_files_to_emails import sharing_file_link
from tg_bot.bot import bot
from tg_bot.markup import cancel_markup, home_markup
from tg_bot.states import UploadStates
from utils import create_user_folder


@bot.message_handler(commands=["start", "help"])
async def start_message(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.reply_to(message, "Hi!\nI'm Google Drive uploader bot.", reply_markup=home_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["menu"])
async def menu_message(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.reply_to(message, "Hi!\nI'm Google Drive uploader bot.", reply_markup=home_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["upload_files"])
async def upload_files_handler(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.direct_upload, message.chat.id)
    await bot.send_message(message.chat.id, "Send files", reply_markup=cancel_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["upload_zip"])
async def zip_file_upload(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.zip_upload, message.chat.id)
    await bot.send_message(message.chat.id, "Send zip file", reply_markup=cancel_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["upload_folder"])
async def upload_files_from_folder(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.folder_upload, message.chat.id)
    await bot.send_message(message.chat.id, "Send path to the folder you want to upload", reply_markup=cancel_markup())


@bot.message_handler(state=UploadStates.folder_upload)
async def process_path(message: telebot.types.Message):
    folder_path = message.text
    drive_folder_name = f"{message.from_user.username}_{datetime.now().strftime('%Y_%m_%d-%I_%M_%S_%p')}"
    folder_id = create_user_folder(drive_folder_name)
    res_msg = await bot.send_message(
        message.chat.id,
        f"Uploading files from {folder_path}",
        reply_markup=telebot.types.ReplyKeyboardRemove(selective=False),
    )
    if folder_path[-1] == os.path.sep:
        paths = [f"{folder_path}{path}" for path in os.listdir(folder_path)]
    else:
        paths = [f"{folder_path}/{path}" for path in os.listdir(folder_path)]
    upload_data_to_drive_zip.upload_files(paths, folder_id)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=res_msg.id, text="Upload completed")
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.send_message(message.chat.id, "Choose next action", reply_markup=home_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["upload_excel"])
async def excel_files_upload(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.excel_upload, message.chat.id)
    await bot.send_message(message.chat.id, "Send excel table file", reply_markup=cancel_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["give_access"])
async def give_access_to_files(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.give_access, message.chat.id)
    await bot.send_message(
        message.chat.id, "Send link to google excel table file with email - file pairs", reply_markup=cancel_markup()
    )


@bot.message_handler(state=UploadStates.give_access)
async def process_link(message: telebot.types.Message):
    result = await bot.send_message(message.chat.id, "Starting to share files")
    sharing_file_link(message.text)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=result.id, text="Files successfully shared")
    await bot.send_message(message.chat.id, "Choose next action", reply_markup=home_markup())


@bot.message_handler(state="*", commands=["to_main_menu"])
async def cancel_pick(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.send_message(message.chat.id, "Choose other option", reply_markup=home_markup())
