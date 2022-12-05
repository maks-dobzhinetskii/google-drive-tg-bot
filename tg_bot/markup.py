import telebot


def home_markup():
    upload_option_kb = telebot.types.ReplyKeyboardMarkup()
    upload_option_kb.row("/upload_files", "/upload_zip", "/upload_folder", "/give_access")
    return upload_option_kb


def cancel_markup():
    cancel_kb = telebot.types.ReplyKeyboardMarkup()
    cancel_kb.row("/to_main_menu")
    return cancel_kb
