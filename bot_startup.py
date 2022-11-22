import asyncio

from telebot import asyncio_filters


if __name__ == "__main__":
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    asyncio.run(bot.polling())
