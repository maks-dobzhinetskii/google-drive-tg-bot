import os
from dotenv import load_dotenv, find_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage


load_dotenv(find_dotenv())

API_TOKEN = os.getenv("API_TOKEN")

bot = AsyncTeleBot(API_TOKEN, state_storage=StateMemoryStorage())
