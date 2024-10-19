import asyncio
import logging
import config
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import webhook_list

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
async def callbacks_num(callback: types.CallbackQuery):

    action = callback.data.split("_")[1]

    if action == "1":
        for i in webhook_list.x:
            if webhook_list.x[i] == 0:
                await callback.message.edit_text(f"Вот ссылка URL '{i}', вставьте её в вебхуки в гитхабе и все, выбрав все ивенты.")
                webhook_list.x[i] = 1
                break

    elif action == "2":
        y = []
        for i in webhook_list.x:
            if webhook_list.x[i] != 0:
                y.append(i)     
        message = ''
        for item in y:
            message += item 
            message += '\n'
        await callback.message.edit_text(f"Список вебхуков: \n{message} ")        


    elif action == "3":
        await callback.message.edit_text("Отправьте ссылку на вебхук")



@dp.message(Command('id'))
async def get_id(message: types.Message):
    await message.answer(f'{message.chat.id}')
    chat_id = message.chat.id
    print(chat_id)

@dp.message(Command('threadid'))
async def get_id(message: types.Message):
    await message.answer(f'{message.message_thread_id}')
    chat_id = message.chat.id
    print(chat_id)

async def webhook_test(message, id = -1002360036125, thread_id = 160):
    await bot.send_message(chat_id = id, text=message, message_thread_id=thread_id)


if __name__ == "__main__":
    asyncio.run(main())