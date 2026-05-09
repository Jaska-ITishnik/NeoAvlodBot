from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_mentors_ikb(mentors: list):
    ikb = InlineKeyboardBuilder()
    buttons = []
    for mentor in mentors:
        buttons.append(
            InlineKeyboardButton(text=mentor['full_name'], callback_data=f"mentor_{mentor['id']}")
        )
    buttons.append(InlineKeyboardButton(text="+Qo'shish", callback_data="add_mentor"))
    ikb.add(*buttons)
    ikb.adjust(1, repeat=True)
    return ikb.as_markup()


def admin_mentor_edit_ikb(mentor_id: int):
    ikb = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text="✏", callback_data=f"edit_mentor_{mentor_id}"),
        InlineKeyboardButton(text="🗑", callback_data=f"delete_mentor_{mentor_id}"),
        InlineKeyboardButton(text="🔙Orqaga", callback_data="back_mentors")
    ]
    ikb.add(*buttons)
    ikb.adjust(2, 1)
    return ikb.as_markup()


def admin_courses_ikb(courses: list):
    ikb = InlineKeyboardBuilder()
    buttons = []
    for course in courses:
        buttons.append(
            InlineKeyboardButton(text=course['title'], callback_data=f"course_{course['id']}")
        )
    buttons.append(InlineKeyboardButton(text="+Qo'shish", style="success", callback_data="add_course"))
    ikb.add(*buttons)
    sizes = [2] * (len(buttons[:-1]) // 2)
    sizes.append(1)
    ikb.adjust(*sizes, repeat=True)
    return ikb.as_markup()
