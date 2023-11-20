import asyncio
import logging
import sys
import requests
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bs4 import BeautifulSoup as bs
from keyboards.admin_kb import main_keyboard, download_keyboard
from database.sqlite_db import start_database, add_to_db, read_db

from config import TOKEN

storage = MemoryStorage()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage, prefix='/')

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    text = State()
    pub_date = State()
    document = State()


@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer(f'Hello, {message.from_user.full_name}', reply_markup=main_keyboard)


@dp.message(Command('Weather'))
async def show_info(message:Message):
    headers_for_parse = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0"
    }
    url = 'https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D1%97%D0%B2'
    parse_url = requests.get(url, headers=headers_for_parse)
    result = bs(parse_url.text, 'html.parser')

    temperature = result.find('p', class_='today-temp').text.strip()
    description = result.find('div', class_='description').text.strip()

    # Creating a message to send to the user
    weather_message = f'The current weather in Kiev:\nTemperature: {temperature}\nDescription: {description}'

    # Sending the weather information to the user
    await message.answer(weather_message, reply_markup=main_keyboard)

@dp.message(Command('Cancel'))
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Введення даних припинено.')


@dp.message(Command('Download'))
async def fs_start(message: Message, state: FSMContext):
    await state.set_state(FSMAdmin.photo)
    await message.answer('Завантажте обкладинку статті \n\n Припинити ввід - /Cancel', reply_markup=download_keyboard)

@dp.message(Command('DownloadFile'))
async def fs_start_document(message: Message, state: FSMContext):
    await state.set_state(FSMAdmin.document)
    await message.answer('Завантажте файл статті\n\nПрипинити ввід - /Cancel', reply_markup=download_keyboard)

@dp.message(FSMAdmin.photo)
async def down_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[0].file_id)
    await state.set_state(FSMAdmin.name)
    await message.answer('Введіть назву статті', reply_markup=download_keyboard)

@dp.message(FSMAdmin.name)
async def down_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FSMAdmin.text)
    await message.answer('Введіть текст статті', reply_markup=download_keyboard)

@dp.message(FSMAdmin.text)
async def down_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(FSMAdmin.pub_date)
    await message.answer('Введіть дату публікації (формат: YYYY-MM-DD)', reply_markup=download_keyboard)

@dp.message(FSMAdmin.pub_date)
async def down_pub_date(message: Message, state: FSMContext):
    pub_date_text = message.text
    await state.update_data(pub_date=message.text)
    data = await state.get_data()
    add_to_db(data)
    await state.clear()
    await message.answer('Complete', reply_markup=main_keyboard)

@dp.message(Command('Show'))
async def show(message:Message):
    data = read_db()
    for i in data:
        await message.answer_photo(i[0],
                                   f'Назва {i[1]}\n Текст {i[2]} \n Дата публікації {i[3]}')


@dp.message(Command('Poem'))
async def cpp_read(message:Message):
    with open('database/poem.txt', 'r') as f:
        text = f.read()
    await message.answer(text, reply_markup=main_keyboard)
#func for start bot
async def main():
    print('BOT online')
    start_database()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())