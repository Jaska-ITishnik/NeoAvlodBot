from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def admin_main_menu_kb():
    kb = ReplyKeyboardBuilder()
    buttons = [
        KeyboardButton(text="📚 Kurslar"),
        KeyboardButton(text="👨‍🏫 Mentorlar"),
        KeyboardButton(text="🏢 Filiallar"),
        KeyboardButton(text="🗓 Guruhlar"),
        KeyboardButton(text="📝 Arizalar"),
        KeyboardButton(text="❓ FAQ"),
        KeyboardButton(text="📊 Statistika")
    ]
    kb.add(*buttons)
    kb.adjust(2, 2, 2, 1)
    return kb.as_markup(resize_keyboard=True)


def admin_add_mentor_kb():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="➕Mentor qo'shish"))
    return kb.as_markup(resize_keyboard=True)
