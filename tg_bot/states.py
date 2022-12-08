from telebot.asyncio_handler_backends import State, StatesGroup


class UploadStates(StatesGroup):
    home_page = State()
    direct_upload = State()
    zip_upload = State()
    folder_upload = State()
    give_access = State()
