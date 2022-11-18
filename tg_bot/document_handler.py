import telebot

from tg_bot.bot import bot
from tg_bot.states import UploadStates

from upload_data_to_drive import upload_files


@bot.message_handler(state=UploadStates.direct_upload, content_types=["document"])
async def handle_direct_upload(message: telebot.types.Message):
    result_message = await bot.send_message(
        message.chat.id, "<i>Downloading your file...</i>", parse_mode="HTML", disable_web_page_preview=True
    )
    file_path = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_path.file_path)
    file_name = file_path.file_path.split("/")[1]
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)

    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=result_message.id, text="<i>Done!</i>", parse_mode="HTML"
    )
    with open(file_name, "rb") as new_file:
        await bot.send_document(message.chat.id, new_file)
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)


@bot.message_handler(state=UploadStates.zip_upload, content_types=["document"])
async def handle_zip_upload(message: telebot.types.Message):
    result_message = await bot.send_message(
        message.chat.id, "<i>Downloading...</i>", parse_mode="HTML", disable_web_page_preview=True
    )
    file_path = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_path.file_path)
    file_name = file_path.file_path.split("/")[1]
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)

    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=result_message.id, text="<i>Done!</i>", parse_mode="HTML"
    )
    with open(file_name, "rb") as new_file:
        await bot.send_document(message.chat.id, new_file)
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)


@bot.message_handler(state=UploadStates.excel_upload, content_types=["document"])
async def handle_excel_upload(message: telebot.types.Message):
    result_message = await bot.send_message(
        message.chat.id, "<i>Downloading...</i>", parse_mode="HTML", disable_web_page_preview=True
    )
    file_path = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_path.file_path)
    file_name = file_path.file_path.split("/")[1]
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)

    upload_files()
    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=result_message.id, text="<i>Done!</i>", parse_mode="HTML"
    )
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
