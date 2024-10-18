import asyncio
import logging
import config
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F



logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher()
user_data = {}

def get_keyboard():
    buttons = [
        [types.InlineKeyboardButton(text="Добавление вебхуков", callback_data="num_1")],
        [types.InlineKeyboardButton(text="Просмотр Вебхуков", callback_data="num_2")],
        [types.InlineKeyboardButton(text="Удаление вебхуков", callback_data="num_3")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def cmd_random(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=get_keyboard())
    

@dp.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):

    action = callback.data.split("_")[1]

    if action == "1":
        await callback.message.edit_text("Отправьте ссылку на вебхук")
    elif action == "2":
        await callback.message.edit_text("Список вебхуков:")
    elif action == "3":
        await callback.message.edit_text("Отправьте ссылку на вебхук")

    await callback.answer()

if __name__ == "__main__":
    asyncio.run(main())