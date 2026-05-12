from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.buttons import admin_mentor_edit_ikb, admin_mentors_ikb, admin_course_edit_ikb, admin_courses_ikb
from bot.states import AddMentorForm, AddCourseForm
from data.base import mentors_db, courses_db

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


@admin_callback_router.callback_query(F.data.startswith("delete_mentor_"))
async def delete_mentor_handler(callback: CallbackQuery):
    mentor_id = int(callback.data.split("_")[-1])
    mentors_db.delete(item_id=mentor_id)
    mentors = mentors_db.get_all()
    await callback.message.delete()
    await callback.answer("Mentor o'chirildi🗑")
    await callback.message.answer("Mentorlar👇", reply_markup=admin_mentors_ikb(mentors))


##############################################################################

@admin_callback_router.callback_query(lambda x: x.data.startswith("course_"))
async def admin_course_handler(callback: CallbackQuery):
    course_id = int(callback.data.split("_")[-1])
    current_course = courses_db.get_by_id(item_id=course_id)
    mentor_ids = current_course['mentor_ids']
    mentor_data = ""
    mentors = mentors_db.get_all()
    for mentor in mentors:
        if mentor['id'] in mentor_ids:
            mentor_data += f"""| {mentor["full_name"]} \n"""
    info = f"""
<b>📛Nomi:</b> {current_course["title"]}
<b>📖Tavsifi:</b> {current_course['description']}
<b>📅Davomiyligi:</b> {current_course['duration']}
<b>💰Narxi:</b> {current_course['price']}
<b>👨🏻‍🏫Mentorlarimiz:</b> {mentor_data}
    """
    await callback.message.delete()
    await callback.message.answer_photo(photo=f"{current_course['photo']}", caption=info, parse_mode=ParseMode.HTML,
                                        reply_markup=admin_course_edit_ikb(current_course['id']))


@admin_callback_router.callback_query(F.data == "back_courses")
async def back_mentors_handler(callback: CallbackQuery):
    courses = courses_db.get_all()
    await callback.message.delete()
    await callback.message.answer("Kurslar👇", reply_markup=admin_courses_ikb(courses))


@admin_callback_router.callback_query(F.data == "add_course")
async def add_mentor_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("""
To'liq nomini kiriting:
<blockquote>Rus tili</blockquote>
    """, parse_mode=ParseMode.HTML)
    await state.set_state(AddCourseForm.title)


@admin_callback_router.callback_query(AddCourseForm.mentor, F.data.startswith("select_mentor_"))
async def select_mentor_handler(callback: CallbackQuery, state: FSMContext):
    mentor_id = int(callback.data.split("_")[-1])
    await state.update_data(mentor_ids=[mentor_id])
    await callback.message.delete()
    await callback.message.answer("Rasmi")
    await state.set_state(AddCourseForm.photo)


@admin_callback_router.callback_query(F.data.startswith("delete_mentor_"))
async def delete_mentor_handler(callback: CallbackQuery):
    mentor_id = int(callback.data.split("_")[-1])
    mentors_db.delete(item_id=mentor_id)
    mentors = mentors_db.get_all()
    await callback.message.delete()
    await callback.answer("Mentor o'chirildi🗑")
    await callback.message.answer("Mentorlar👇", reply_markup=admin_mentors_ikb(mentors))
