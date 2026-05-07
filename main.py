import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommand

from bot.buttons import admin_main_menu_kb, user_main_menu_kb
from bot.handlers import admin_message_router, admin_callback_router
from config import TOKEN, ADMINS

dp = Dispatcher()


# class RegistrationForm(StatesGroup):
#     course = State()
#     phone = State()
#     full_name = State()
#     dob = State()
#
#
# ABOUT_COURSES = """
# <b>NEOAVLOD MARKAZIMIZ KURSLARI</b>
#
# <b>Python (Web yo‘nalish)</b>
# Davomiyligi: 9 oy
# To‘lov: oyiga 650 000 so‘m
# Yo‘nalish: Web dasturlashga asoslangan
# Siz nimalarni o‘rganasiz?
#
# • Python dasturlash asoslari
# • Web saytlar yaratish
# • Backend dasturlash
# • Real loyihalar bilan ishlash
#
# <b>Ingliz tili (Best of the Best)</b>
# Davomiyligi: 9 oy
# To‘lov: oyiga 450 000 so‘m
# Kurs afzalliklari:
#
# • Zamonaviy metodika
# • Speaking, Listening, Reading, Writing ko‘nikmalari
# • Tajribali ustozlar
# • IELTS ga tayyorlov
#
# <b>Yapon tili</b>
# Davomiyligi: (individual belgilanadi)
# To‘lov: (aniqlashtiriladi)
# Kurs davomida:
#
# • Yapon alifbolari (Hiragana, Katakana, Kanji)
# • Kundalik suhbatlashuv
# • Yapon madaniyati bilan tanishuv
# • Boshlang‘ichdan yuqori darajagacha o‘rganish imkoniyati
#
# <b>Kiber xavfsizlik (Cyber Security)</b>
# To‘lov: oyiga 500 000 so‘m
# Siz nimalarni o‘rganasiz?
#
# • Internet xavfsizligi asoslari
# • Tizimlarni himoyalash
# • Hackerlik tushunchalari (ethical hacking)
# • Amaliy mashg‘ulotlar
#
# <b>Biz bilan kelajagingizni bugundan boshlang!</b>
# Batafsil ma’lumot uchun bog‘laning!
# Joylar soni cheklangan!
# """
#
#
# @dp.message(Command(commands=["help"]))
# async def help_handler(message: Message):
#     await message.answer("""
# /start --- <blockquote>Botni ishga tushurish🛫</blockquote>
# /help --- <blockquote>Bot uchun yoriqnoma📖</blockquote>
#     """, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.from_user.id in ADMINS:
        await message.answer("Assalomu aleykum <b>ADMIN</b> xush kelibsiz!",
                             reply_markup=admin_main_menu_kb(), parse_mode=ParseMode.HTML)
    else:
        await message.answer("Assalomu aleykum <b>NEOAVLOD</b> o'quv markazi rasmiy botiga xush kelibsiz!",
                             reply_markup=user_main_menu_kb(), parse_mode=ParseMode.HTML)


async def on_startup(bot: Bot):
    commands = [
        BotCommand(command="start", description="Botni ishga tushurish"),
        BotCommand(command="help", description="Bot haqida batafsil"),
        BotCommand(command="xatolik_haqida", description="Hatolik haqida ogohlantirish"),
        BotCommand(command="botirjon", description="Hatolik haqida ogohlantirish"),
    ]
    await bot.set_my_commands(commands)


async def on_shutdown(bot: Bot):
    await bot.delete_my_commands()


async def main() -> None:
    bot = Bot(token=TOKEN)
    dp.include_routers(admin_message_router, admin_callback_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
