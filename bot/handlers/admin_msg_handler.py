from aiogram import Router, F
from aiogram.enums import ContentType, ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.buttons import admin_mentors_ikb, admin_courses_ikb, admin_mentors_select_ikb
from bot.filters import IsAdmin
from bot.states import AddMentorForm, AddCourseForm
from config import ADMINS
from data.base import mentors_db, courses_db

admin_message_router = Router()


@admin_message_router.message(IsAdmin(ADMINS), F.text == "📚 Kurslar")
async def courses_handler(message: Message):
    courses = courses_db.get_all()
    await message.answer("Kurslar👇", reply_markup=admin_courses_ikb(courses))


@admin_message_router.message(IsAdmin(ADMINS), F.text == "👨‍🏫 Mentorlar")
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


@admin_message_router.message(AddCourseForm.title)
async def course_title_handler(message: Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    await message.answer("""
Tavsifini kiriting
<blockquote>Bu kursdan ko'p bilim olasiz!</blockquote>
""", parse_mode=ParseMode.HTML)
    await state.set_state(AddCourseForm.description)


@admin_message_router.message(AddCourseForm.description)
async def course_description_handler(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer("""
Narxini kiriting so'mda
<blockquote>450000</blockquote>
""", parse_mode=ParseMode.HTML)
    await state.set_state(AddCourseForm.price)


@admin_message_router.message(AddCourseForm.price)
async def course_price_handler(message: Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    await message.answer("""
Davomiyligi
<blockquote>9 oy</blockquote>
""", parse_mode=ParseMode.HTML)
    await state.set_state(AddCourseForm.duration)


@admin_message_router.message(AddCourseForm.duration)
async def course_price_handler(message: Message, state: FSMContext):
    duration = message.text
    await state.update_data(duration=duration)
    mentors = mentors_db.get_all()
    await message.answer("Mentorlarni tanlang👇", reply_markup=admin_mentors_select_ikb(mentors))
    await state.set_state(AddCourseForm.mentor)


@admin_message_router.message(AddCourseForm.photo, F.photo)
async def course_price_handler(message: Message, state: FSMContext):
    photo = message.photo[0].file_id
    await state.update_data(photo=photo)
    data = await state.get_data()
    new_course = {
        "title": data["title"],
        "description": data["description"],
        "price": data["price"],
        "duration": data["duration"],
        "mentor_ids": data["mentor_ids"],
        "photo": data["photo"]
    }
    courses_db.create(new_course)
    await message.answer("Kurs muvoffaqiyatliy qo'shildi✅")
