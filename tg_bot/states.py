from telebot.asyncio_handler_backends import State, StatesGroup


class UploadStates(StatesGroup):
    home_page = State()
    drive_management = State()
    direct_upload = State()
    zip_upload = State()
    give_access = State()
    setting_expiration = State()
