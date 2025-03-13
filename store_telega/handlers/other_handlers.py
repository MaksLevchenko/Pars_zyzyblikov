from aiogram import Router
from aiogram.fsm.state import default_state
from aiogram.types import Message
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext


router = Router()


# Этот хэндлер будет срабатывать если вводить что-то не тогда, когда просят
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    """Этот хэндлер будет срабатывать если вводить что-то не тогда, когда просят"""
    await message.reply(text="Извините, я Вас не понял.")


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands="cancel"), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    """Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
    кроме состояния по умолчанию, и отключать машину состояний"""
    await message.answer(text="Всё успешно отменено!")
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()
