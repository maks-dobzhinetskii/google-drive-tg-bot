import asyncio
import telebot

from dotenv import load_dotenv, find_dotenv
from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup

from upload_data_to_drive import upload_files
from sharing_files_to_emails import sharing_file_link


load_dotenv(find_dotenv())

API_TOKEN = "5643080489:AAGYqY7j1bMdU_jwjhm67Xw4Uy3RB5qEWjw"

bot = AsyncTeleBot(API_TOKEN, state_storage=StateMemoryStorage())


class UploadStates(StatesGroup):
    home_page = State()
    direct_upload = State()
    zip_upload = State()
    folder_upload = State()
    excel_upload = State()
    give_access = State()


# Keyboard markups

def home_markup():
    upload_option_kb = telebot.types.ReplyKeyboardMarkup()
    upload_option_kb.row("/upload_files", "/upload_zip", "/upload_folder", "/upload_excel", "/give_access")
    return upload_option_kb


def cancel_markup():
    cancel_kb = telebot.types.ReplyKeyboardMarkup()
    cancel_kb.row("/to_main_menu")
    return cancel_kb


# Message handlers

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
    await message.media_group_id


@bot.message_handler(state=UploadStates.home_page, commands=["upload_folder"])
async def upload_files_from_folder(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.folder_upload, message.chat.id)
    await bot.send_message(message.chat.id, "Send path to the folder you want to upload", reply_markup=cancel_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["upload_excel"])
async def excel_files_upload(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.excel_upload, message.chat.id)
    await bot.send_message(message.chat.id, "Send excel table file", reply_markup=cancel_markup())


@bot.message_handler(state=UploadStates.home_page, commands=["give_access"])
async def give_access_to_files(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.give_access, message.chat.id)
    await bot.send_message(message.chat.id, "Send link to google excel table file with email - file pairs", reply_markup=cancel_markup())
    sharing_file_link()
    await bot.send_message(message.chat.id, "")


@bot.message_handler(state="*", commands=["to_main_menu"])
async def cancel_pick(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.send_message(message.chat.id, "Choose other option", reply_markup=home_markup())


# Document handlers

@bot.message_handler(state=UploadStates.direct_upload, content_types=["document"])
async def handle_direct_upload(message: telebot.types.Message):
    result_message = await bot.send_message(message.chat.id, "<i>Downloading your file...</i>", parse_mode="HTML", disable_web_page_preview=True)
    file_path = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_path.file_path)
    file_name = file_path.file_path.split("/")[1]
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=result_message.id, text="<i>Done!</i>", parse_mode="HTML")
    with open(file_name, "rb") as new_file:
        await bot.send_document(message.chat.id, new_file)
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)


@bot.message_handler(state=UploadStates.zip_upload, content_types=["document"])
async def handle_zip_upload(message: telebot.types.Message):
    result_message = await bot.send_message(message.chat.id, "<i>Downloading...</i>", parse_mode="HTML", disable_web_page_preview=True)
    file_path = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_path.file_path)
    file_name = file_path.file_path.split("/")[1]
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)

    await bot.edit_message_text(chat_id=message.chat.id, message_id=result_message.id, text="<i>Done!</i>", parse_mode="HTML")
    with open(file_name, "rb") as new_file:
        await bot.send_document(message.chat.id, new_file)
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)


@bot.message_handler(state=UploadStates.excel_upload, content_types=["document"])
async def handle_excel_upload(message: telebot.types.Message):
    result_message = await bot.send_message(message.chat.id, "<i>Downloading...</i>", parse_mode="HTML", disable_web_page_preview=True)
    file_path = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_path.file_path)
    file_name = file_path.file_path.split("/")[1]
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)

    upload_files()
    await bot.edit_message_text(chat_id=message.chat.id, message_id=result_message.id, text="<i>Done!</i>", parse_mode="HTML")
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)


if __name__ == "__main__":
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    asyncio.run(bot.polling())
