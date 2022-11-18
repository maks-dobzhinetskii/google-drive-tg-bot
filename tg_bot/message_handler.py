import telebot

from tg_bot.bot import bot
from tg_bot.markup import cancel_markup, home_markup
from tg_bot.states import UploadStates

from sharing_files_to_emails import sharing_file_link


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
    await bot.send_message(message.chat.id, "Done!")


@bot.message_handler(state="*", commands=["to_main_menu"])
async def cancel_pick(message: telebot.types.Message):
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.send_message(message.chat.id, "Choose other option", reply_markup=home_markup())
