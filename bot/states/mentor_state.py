from aiogram.fsm.state import StatesGroup, State


class AddMentorForm(StatesGroup):
    full_name = State()
    position = State()
    experience = State()
    photo = State()
