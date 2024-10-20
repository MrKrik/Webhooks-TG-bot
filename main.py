import asyncio
import logging
import config
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
# import webhook_list
# import db

logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
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
async def callbacks_num(callback: types.CallbackQuery, ):

    action = callback.data.split("_")[1]

    if action == "1":
        url = db.create(callback.message.from_user.id)
        await callback.message.edit_text(f"Вот ссылка URL '( {url} )', вставьте её в вебхуки в гитхабе и все, выбрав все ивенты.")

    elif action == "2":
        y = db.show(callback.message.from_user.id)
        message = '' 
        for item in y:
            message += item 
            message += '\n'
        await callback.message.edit_text(f"Список вебхуков: \n{message} ")        


    elif action == "3":
        await callback.message.edit_text("Отправьте ссылку на вебхук")

@dp.message(F.text.startswith("http://127.0.0.1:5000/webhooks/"))
async def show(message: types.Message):
    db.delete(message, message.from_user.id)
    await message.answer("Сообщение удалено")
    


@dp.message(Command('id'))
async def get_id(message: types.Message):
    print(message.from_user.id)
    await message.answer(f'{message.chat.id}')
    chat_id = message.chat.id
    print(chat_id)

@dp.message(Command('threadid'))
async def get_id(message: types.Message):
    await message.answer(f'{message.message_thread_id}')
    chat_id = message.chat.id
    print(chat_id)

@dp.message(Command('user'))
async def get_id(message: types.Message):
    await message.answer(f'{message.chat.id}')

async def webhook_test(message, id = -1002360036125, thread_id = 160):
    await bot.send_message(chat_id = id, text=message, message_thread_id=thread_id)


if __name__ == "__main__":
    asyncio.run(main())