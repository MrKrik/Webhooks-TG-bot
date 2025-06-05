from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import types, F, Router
from random import choices
import string
import tests.config as config
import bot.db as db

router = Router()


class CreateWebhook(StatesGroup):
    name = State()
    channel_id = State()
    thread_id = State()
    user_id = State()

def webhook_create(name,user_id, channel_id, thread_id):
    server_url = config.URL
    random_url = ''.join(choices(string.ascii_letters,k=20))
    full_url = server_url+'github-webhook/'+random_url
    db.add(name=name,url=random_url, channel_id=channel_id, thread_id=thread_id, author_id=user_id)
    return full_url

@router.callback_query(F.data == "create_webhhok")
async def catch_channel_id(callback: types.CallbackQuery, state:FSMContext):
    await callback.answer()
    await state.set_state(CreateWebhook.name)
    await callback.message.answer("Введите название вашего вебхука")

@router.message(CreateWebhook.name)
async def catch_channel_id(message: types.Message, state:FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(CreateWebhook.channel_id)
    await message.answer("Введите id вашего чата, вы можете узнать его написав /id")

@router.message(CreateWebhook.channel_id)
async def get_thread_id(message: types.Message, state:FSMContext):
    await state.update_data(channel_id = message.text, user_id = message.from_user.id)
    await message.answer('Если вы хотите использовать бота на форуме введите id вашей ветки, вы можете узнать его написав /threadid\nЕсли его нету напишите None')
    await state.set_state(CreateWebhook.thread_id)

@router.message(CreateWebhook.thread_id)
async def send_webhhok(message: types.Message, state: FSMContext):
    await state.update_data(thread_id = message.text)
    data = await state.get_data()
    webhook = webhook_create(name= data['name'],user_id= data['user_id'],channel_id= data['channel_id'],thread_id= data['thread_id'])
    await message.answer(f'Вот ваш url {webhook}\nВставьте его в настройка репозитория гитхаба установив:\nContent-type: application/json')
    await state.clear()