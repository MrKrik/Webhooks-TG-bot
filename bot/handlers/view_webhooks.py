from aiogram import types, F, Router
import db

router = Router()

@router.callback_query(F.data == "view_webhooks")
async def view_webhooks(callback: types.CallbackQuery):
    buttons = []
    buttons_name = db.get_user_webhooks(callback.message.chat.id)
    for name in buttons_name:
        [types.InlineKeyboardButton(text=name['webhook_name'], callback_data='webhook')]
        buttons.append([types.InlineKeyboardButton(text=name['webhook_name'], callback_data='webhook_'+name['webhook_name'])])
    buttons.append([types.InlineKeyboardButton(text='Назад', callback_data='main_menu')])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text='Список вебхуков', reply_markup=keyboard)

@router.callback_query(F.data.startswith("webhook_"))
async def view_webhooks_information(callback: types.CallbackQuery):
    webhook_name = callback.data.split("_")[1]
    buttons = [[types.InlineKeyboardButton(text='Удалить вебхук', callback_data='webhookdelete_'+webhook_name)],
               [types.InlineKeyboardButton(text='Назад', callback_data='view_webhooks')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(db.get_webhooks_info(webhook_name=webhook_name),reply_markup=keyboard)

@router.callback_query(F.data.startswith("webhookdelete"))
async def delete_webhook(callback: types.CallbackQuery):
    webhook_name = callback.data.split("_")[1]
    db.delete_webhook(webhook_name)
    buttons = [[types.InlineKeyboardButton(text='Назад', callback_data='view_webhooks')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text('Вебхук удален',reply_markup=keyboard)