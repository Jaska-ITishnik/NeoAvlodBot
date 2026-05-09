from aiogram.fsm.state import StatesGroup, State


class AddCourseForm(StatesGroup):
    title = State()
    description = State()
    price = State()
    duration = State()
    level = State()
    photo = State()
