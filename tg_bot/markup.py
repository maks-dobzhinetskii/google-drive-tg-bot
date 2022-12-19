import telebot


def home_markup():
    upload_option_kb = telebot.types.ReplyKeyboardMarkup()
    upload_option_kb.row("/upload_files", "/upload_zip", "/give_access", "/drive_management")
    return upload_option_kb


def cancel_markup():
    cancel_kb = telebot.types.ReplyKeyboardMarkup()
    cancel_kb.row("/to_main_menu")
    return cancel_kb


def drive_management_markup():
    drive_management_kb = telebot.types.ReplyKeyboardMarkup()
    drive_management_kb.row("/delete_expired", "/clear_all")
    return drive_management_kb
