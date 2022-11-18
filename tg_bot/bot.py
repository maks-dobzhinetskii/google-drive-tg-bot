from dotenv import load_dotenv, find_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage


load_dotenv(find_dotenv())

API_TOKEN = "5643080489:AAGYqY7j1bMdU_jwjhm67Xw4Uy3RB5qEWjw"

bot = AsyncTeleBot(API_TOKEN, state_storage=StateMemoryStorage())
