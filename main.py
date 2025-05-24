import asyncio
import logging
import config
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F
from aiogram.utils.markdown import link
from handlers import create_webhook, view_webhooks
from keyboards import menu
from aiogram import types
import db


logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
bot = Bot(token=config.TOKEN)
dp = Dispatcher()
user_data = {}

@dp.message(CommandStart())
async def cmd_random(message: types.Message, state:FSMContext):
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=menu.menu_keyboard())

@dp.callback_query(F.data == "main_menu")
async def go_main_menu(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите действие:", reply_markup=menu.menu_keyboard())

@dp.message(Command('id'))
async def get_id(message: types.Message):
    print(message.from_user.id)
    await message.answer(f'{message.chat.id}')

@dp.message(Command('threadid'))
async def get_id(message: types.Message):
    await message.answer(f'{message.message_thread_id}')

@dp.message(Command('user'))
async def get_id(message: types.Message):
    await message.answer(f'{message.chat.id}')

async def webhook_send(message, channel_id = -1002360036125, thread_id = 160, web_preview = True):
    await bot.send_message(chat_id = channel_id, text=message, message_thread_id=thread_id, disable_web_page_preview=web_preview, parse_mode='MARKDOWN')

async def main():
    dp.include_router(create_webhook.router)
    dp.include_router(view_webhooks.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())