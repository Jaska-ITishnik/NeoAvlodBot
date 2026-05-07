from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.buttons import admin_mentor_edit_ikb, admin_mentors_ikb
from bot.states import AddMentorForm
from data.base import mentors_db

admin_callback_router = Router()


@admin_callback_router.callback_query(lambda x: x.data.startswith("mentor_"))
async def admin_mentor_handler(callback: CallbackQuery):
    mentor_id = int(callback.data.split("_")[-1])
    current_mentor = mentors_db.get_by_id(item_id=mentor_id)
    info = f"""
<b>📛Ismi:</b> {current_mentor["full_name"]}
<b>👷Lavozimi:</b> {current_mentor['position']}
<b>🔢Tajribasi:</b> {current_mentor['experience']}
    """
    await callback.message.delete()
    await callback.message.answer_photo(photo=f"{current_mentor['photo_id']}", caption=info, parse_mode=ParseMode.HTML,
                                        reply_markup=admin_mentor_edit_ikb(current_mentor['id']))


@admin_callback_router.callback_query(F.data == "back_mentors")
async def back_mentors_handler(callback: CallbackQuery):
    mentors = mentors_db.get_all()
    await callback.message.delete()
    await callback.message.answer("Mentorlar👇", reply_markup=admin_mentors_ikb(mentors))


@admin_callback_router.callback_query(F.data == "add_mentor")
async def add_mentor_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("""
To'liq ismini kiriting:
<blockquote>Jamol Kamolov</blockquote>
    """)
    await state.set_state(AddMentorForm.full_name)
