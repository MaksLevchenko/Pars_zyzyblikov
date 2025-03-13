from bot import all_media_dir
from config.config import load_config

from store_telega.state import *
from store_telega.logic import pars_file

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state


router = Router()

config = load_config()


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands="cancel"), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text="Отменять нечего.")


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text="Всё успешно отменено!")
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@router.message(Command(commands="get_price"))
async def start_command(message: Message, state: FSMContext):
    """Срабатывает при нажатии команды '/get_price' и предлагает загрузить файл"""

    await message.answer(text="Пожалуйста отправте файл")
    await state.set_state(FSMFile.upload)


@router.message(StateFilter(FSMFile.upload))
async def process_file(message: Message, state: FSMContext):
    """Обрабатывает загруженный файл"""

    file_id = message.document.file_id
    file_name = message.document.file_name
    file = await message.bot.get_file(file_id)

    file_path = await message.bot.download_file(
        file.file_path, f"{all_media_dir}/{file_name}"
    )
    data = await pars_file(filename=file_name)
    for store in data:
        await message.answer(
            f"В магазине: {store['title']}\nЦена зюзюблика: {store['price']}"
        )
    await state.set_state(default_state)
