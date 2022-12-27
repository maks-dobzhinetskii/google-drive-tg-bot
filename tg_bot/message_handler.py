import telebot

from logs.logger import log
from google_utils import drive
from tg_bot.bot import bot
from tg_bot.markup import cancel_markup, drive_management_markup, home_markup
from tg_bot.states import UploadStates


@bot.message_handler(commands=["start", "help"])
async def start_message(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.reply_to(message, "Hi!\nI'm Google Drive uploader bot.", reply_markup=home_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["menu"])
async def menu_message(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.reply_to(message, "Hi!\nI'm Google Drive uploader bot.", reply_markup=home_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["drive_management"])
async def drive_management_handler(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.drive_management, message.chat.id)
    await bot.reply_to(message, "Choose management tool", reply_markup=drive_management_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["upload_files"])
async def upload_files_handler(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.direct_upload, message.chat.id)
    await bot.send_message(message.chat.id, "Send files", reply_markup=cancel_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["upload_zip"])
async def zip_file_upload(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.zip_upload, message.chat.id)
    await bot.send_message(message.chat.id, "Send zip file", reply_markup=cancel_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["give_access"])
async def give_access_to_files(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.give_access, message.chat.id)
    await bot.send_message(
        message.chat.id, "Send link to google excel table file with email - file pairs", reply_markup=cancel_markup()
    )


@bot.message_handler(state=UploadStates.give_access)
async def process_link(message: telebot.types.Message):
    spreadsheet_link = message.text
    log.info("Giving access rights based on google spreadsheet ", spreadsheet_link=spreadsheet_link)
    result = await bot.send_message(message.chat.id, "Starting to share files")
    files_folder_mapped = {}
    folders = drive.get_user_folders(message.from_user.username)
    for folder in folders["files"]:
        if message.from_user.username in folder["name"]:
            files = tuple(file["name"] for file in drive.get_files_from_folder(folder["id"])["files"])
            files_folder_mapped[files] = folder["id"]
    print(files_folder_mapped)
    drive.share_files(spreadsheet_link, files_folder_mapped)
    log.info("Access rights from were granted successfully", spreadsheet_link=spreadsheet_link)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=result.id, text="Files successfully shared")
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.send_message(message.chat.id, "Choose next action", reply_markup=home_markup())


@bot.message_handler(state="*", commands=["to_main_menu"])
async def cancel_pick(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.send_message(message.chat.id, "Choose other option", reply_markup=home_markup())
