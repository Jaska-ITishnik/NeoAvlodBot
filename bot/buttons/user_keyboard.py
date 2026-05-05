from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def user_main_menu_kb():
    kb = ReplyKeyboardBuilder()
    buttons = [
        KeyboardButton(text="📚 Kurslar"),
        KeyboardButton(text="👨‍🏫 Mentorlar"),
        KeyboardButton(text="🏢 Filiallar"),
        KeyboardButton(text="🗓 Ochiq guruhlar"),
        KeyboardButton(text="📝 Demo darsga yozilish"),
        KeyboardButton(text="❓ FAQ"),
        KeyboardButton(text="🌐 Til"),
        KeyboardButton(text="📞 Aloqa")
    ]
    kb.add(*buttons)
    kb.adjust(2, 2, 2, 1)
    return kb.as_markup(resize_keyboard=True)
