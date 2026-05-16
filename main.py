import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommand, CallbackQuery

from bot.buttons import admin_main_menu_kb, user_main_menu_kb
from bot.handlers import admin_message_router, admin_callback_router
from bot.middlewares import JoinRequirementMiddleware
from config import TOKEN, ADMINS

dp = Dispatcher()


@dp.callback_query(F.text == "is_join_chekker")
async def handle_check_if_subscribed(callback_query: CallbackQuery):
    await callback_query.answer("Tekshirish bosildi ✅")


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
    dp.update.outer_middleware.register(JoinRequirementMiddleware())
    dp.include_routers(admin_message_router, admin_callback_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
