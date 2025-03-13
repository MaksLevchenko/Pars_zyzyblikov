from aiogram.fsm.state import State, StatesGroup


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFile(StatesGroup):
    upload = State()  # Состояние ожидания файла
