# -*- coding: utf-8 -*-
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BOT_TOKEN
from database import create_db

# ✅ Bot setup
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

CHANNEL_USERNAME = '@abdulloh_hasaniy'


# ✅ STATES
class Register(StatesGroup):
    gender = State()


# ✅ START command
@dp.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    gender_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Erkak"), KeyboardButton(text="Ayol")]],
        resize_keyboard=True, one_time_keyboard=True
    )
    await message.answer(
        "Assalamu alaykum\n\n\"Tabiiy ovoz va maqomat sirlari\" online kursiga xush kelibsiz.\n\nJinsingizni tanlang:",
        reply_markup=gender_kb
    )
    await state.set_state(Register.gender)


# ✅ JINS tanlangandan so‘ng
@dp.message(Register.gender)
async def gender_chosen(message: types.Message, state: FSMContext):
    if message.text not in ["Erkak", "Ayol"]:
        await message.answer("Iltimos, faqat 'Erkak' yoki 'Ayol' deb tanlang.")
        return
    await state.update_data(gender=message.text)
    await ask_subscription(message)


# ✅ Obuna so‘rovi
async def ask_subscription(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub")]
    ])
    await message.answer("Abdulloh Hasaniy kanaliga obuna bo'lganmisiz?", reply_markup=kb)


# ✅ Obunani tekshiruvchi tugma
@dp.callback_query(F.data == "check_sub")
async def check_subscription(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)

    if member.status in ["member", "administrator", "creator"]:
        await callback.message.answer("✅ Obuna tasdiqlandi!")

        # ✅ New single button
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎤 Jonli individual darslar", callback_data="jonli_darslar")]
        ])
        await callback.message.answer("📌 Hozirda mavjud online kurslar:", reply_markup=kb)
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Obuna bo'lish", url="https://t.me/abdulloh_hasaniy")],
            [InlineKeyboardButton(text="✅ Obuna bo‘ldim", callback_data="check_sub")]
        ])
        await callback.message.answer("❌ Siz Abdulloh Hasaniy kanaliga obuna bo'lmagansiz.", reply_markup=kb)
        await callback.answer("Obuna topilmadi.")


# ✅ Jonli darslar tugmasi uchun handler
@dp.callback_query(F.data == "jonli_darslar")
async def show_individual_lessons(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    gender = data.get("gender", "Erkak")

    if gender == "Ayol":
        text = """👩 Individual yondashuv tarifi

🔹 8 ta jonli dars (haftasiga 2 marta)
🔹 Har bir dars Abdulloh Hasaniy va ayol ustoza tomonidan yopiq kanalda jonli tarzda o‘tiladi
🔹 Yakka tartibda topshiriqlar, ovoz tahlili, shaxsiy maslahatlar 
🔹 Talabaga xos individual yondashuv
🔹 Eng faol ishtrokchilarni sertifikat bilan taqdirlanadi.
🔹 Eng iste'dodli talabalar uchun jamoamizda Ustoz lavozimida faoliyat olib borish imkoniyati 

💳 Narxi: 899 ming so’m"""
    else:
        text = """👨 Individual yondashuv tarifi

🔹 8 ta jonli dars (haftasiga 2 marta)
🔹 Har bir dars Abdulloh Hasaniy tomonidan o‘tiladi
🔹 Darslar yopiq kanalda jonli tarzida o’tiladi
🔹 Yakka tartibda topshiriqlar, ovoz tahlili, shaxsiy maslahatlar 
🔹 Talabaga xos individual yondashuv
🔹 Eng faol ishtrokchilarni sertifikat bilan taqdirlanadi.
🔹 Eng iste'dodli talabalar uchun jamoamizda Ustoz lavozimida faoliyat olib borish imkoniyati 

💳 Narxi: 899 ming so’m"""

    admin_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Admin 1", url="https://t.me/hasaniy_admin1")],
        [InlineKeyboardButton(text="👤 Admin 2", url="https://t.me/hasaniy_admin2")],
        [InlineKeyboardButton(text="👤 Admin 3", url="https://t.me/hasaniy_admin3")]
    ])
    await callback.message.answer(text, reply_markup=admin_kb)
    await callback.answer()


# ✅ RUN
async def main():
    await create_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
