from aiogram import Router, F
from aiogram.enums import ContentType, ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons import admin_mentors_ikb, admin_courses_ikb
from bot.states import AddMentorForm
from data.base import mentors_db, courses_db

admin_message_router = Router()


@admin_message_router.message(F.text == "📚 Kurslar")
async def courses_handler(message: Message):
    courses = courses_db.get_all()
    await message.answer("Kurslar👇", reply_markup=admin_courses_ikb(courses))


@admin_message_router.message(F.text == "👨‍🏫 Mentorlar")
async def admin_mentors_handler(message: Message):
    mentors = mentors_db.get_all()
    await message.answer("Mentorlar👇", reply_markup=admin_mentors_ikb(mentors))


@admin_message_router.message(AddMentorForm.full_name)
async def full_name_handler(message: Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await state.set_state(AddMentorForm.position)
    await message.answer("""
Kasbi:
<blockquote>Masalan: Dasturchi</blockquote>
""", parse_mode=ParseMode.HTML)


@admin_message_router.message(AddMentorForm.position)
async def full_name_handler(message: Message, state: FSMContext):
    position = message.text
    await state.update_data(position=position)
    await state.set_state(AddMentorForm.experience)
    await message.answer("""
Tajribasi:
<blockquote>Masalan: 5 yil</blockquote>
""", parse_mode=ParseMode.HTML)


@admin_message_router.message(AddMentorForm.position)
async def full_name_handler(message: Message, state: FSMContext):
    position = message.text
    await state.update_data(position=position)
    await state.set_state(AddMentorForm.experience)
    await message.answer("""
Tajribasi:
<blockquote>Masalan: 5 yil</blockquote>
""", parse_mode=ParseMode.HTML)


@admin_message_router.message(AddMentorForm.experience)
async def full_name_handler(message: Message, state: FSMContext):
    experience = message.text
    await state.update_data(experience=experience)
    await state.set_state(AddMentorForm.photo)
    await message.answer("Rasmni yuboring:")


@admin_message_router.message(AddMentorForm.photo, F.content_type == ContentType.PHOTO)
async def full_name_handler(message: Message, state: FSMContext):
    photo = message.photo[0].file_id
    await state.update_data(photo=photo)
    data = await state.get_data()
    new_mentor = {
        "full_name": f"{data['full_name']}",
        "position": f"{data['position']}",
        "experience": f"{data['experience']}",
        "course_ids": [],
        "photo_id": f"{data['photo']}"
    }
    mentors_db.create(item=new_mentor)
    await message.answer("Mentor muvofaqqiyatliy qo'shildi✅")
