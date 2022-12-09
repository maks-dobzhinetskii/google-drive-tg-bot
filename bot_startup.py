import asyncio

from tg_bot import document_handler
from tg_bot import message_handler
from tg_bot import drive_handlers

from telebot import asyncio_filters

from tg_bot.bot import bot


if __name__ == "__main__":
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    asyncio.run(bot.polling())
    bot.close()
