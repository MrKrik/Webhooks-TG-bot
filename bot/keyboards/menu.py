from aiogram import types


def menu_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Создать вебхук", callback_data="create_webhhok")],
        [types.InlineKeyboardButton(text="Просмотр вебхуков", callback_data="view_webhooks")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard