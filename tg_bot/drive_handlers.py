import telebot

from logs.logger import log
from google_utils import drive
from tg_bot.bot import bot
from tg_bot.markup import cancel_markup, home_markup
from tg_bot.states import UploadStates


@bot.message_handler(state=UploadStates.drive_management, commands=["delete_expired"])
async def set_expiration_handler(message: telebot.types.Message):
    await bot.send_message(
        message.chat.id,
        "Send files lifetime (in days)\nBot will delete expired files from drive",
        reply_markup=cancel_markup(),
    )
    await bot.set_state(message.from_user.id, UploadStates.setting_expiration, message.chat.id)


@bot.message_handler(state=UploadStates.setting_expiration)
async def delete_expired(message: telebot.types.Message):
    if not message.text.isnumeric():
        await bot.send_message(message.chat.id, "Message must contain only one integer")
        await bot.send_message(
            message.chat.id, "Message must contain only one integer\nChoose other option", reply_markup=home_markup()
        )
        await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
        return
    log.info("Deleting expired files; ", expiration_time=int(message.text), type="days")
    result_message = await bot.send_message(message.chat.id, "Deleting expired files...")
    drive.delete_expired_files(int(message.text))
    log.info("Successfully deleted expired files; ", expiration_time=int(message.text), type="days")
    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=result_message.id, text="Successfully deleted expired files"
    )
    await bot.send_message(message.chat.id, "Choose next action", reply_markup=home_markup())
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)


@bot.message_handler(state=UploadStates.drive_management, commands=["clear_all"])
async def clear_all_files(message: telebot.types.Message):
    log.info("Deleting all files!")
    result_message = await bot.send_message(message.chat.id, "Deleting all files...")
    drive.delete_all_files(drive.get_all_files())
    log.info("All files deleted")
    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=result_message.id, text="Successfully deleted all files\nChoose next action"
    )
    await bot.set_state(message.from_user.id, UploadStates.home_page, message.chat.id)
    await bot.send_message(message.chat.id, "Choose next action", reply_markup=home_markup())
