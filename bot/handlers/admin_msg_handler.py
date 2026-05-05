from aiogram import Router, F
from aiogram.types import Message

admin_router = Router()


@admin_router.message(F.text == "📚 Kurslar")
async def courses_handler(message: Message):
    await message.answer("📚 Kurslar bosildi")
