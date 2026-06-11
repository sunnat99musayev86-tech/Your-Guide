import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from gtts import gTTS
import google.generativeai as genai

# Вставьте ваши реальные ключи прямо в кавычки
API_TOKEN = '8980910424:AAFRqavkI1LjR2-7Q7el29UXBJdhsB9HppI'
genai.configure(api_key='AQ.Ab8RN6KsSn51T1Ve5s_ikreAYfSoml7kIFwK8DawqVmdSBYReA')

model = genai.GenerativeModel('gemini-pro')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def get_main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📍 Где я?", callback_data="loc_info"),
        InlineKeyboardButton("📸 Фото-перевод", callback_data="photo_trans"),
        InlineKeyboardButton("🌍 Переводчик", callback_data="translate"),
        InlineKeyboardButton("📤 Поделиться", callback_data="share")
    )
    return markup

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("✨ Привет! Я твой личный гид.", reply_markup=get_main_menu())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
